import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine

import aio_pika
import msgpack
from aio_pika import Message
from aio_pika.abc import AbstractQueue
from aio_pika.exceptions import QueueEmpty

from src.apps.consumers.base.rabbit_base import RabbitBase
from src.apps.consumers.common.analytics import (
    DECLARE_QUEUE_LATENCY,
    PROCESSING_MESSAGE_LATENCY,
    PRODUCE_MESSAGE_LATENCY,
    TOTAL_CONSUMER_RECEIVE_MESSAGES,
)
from src.core.utils.time import analyze_execution_time

logger = logging.getLogger(__name__)


class BaseConsumer(RabbitBase, ABC):

    __exchange_name__: str

    __RETRIES = 5

    async def declare_exchange(self) -> None:
        channel = await self.channel()
        await channel.declare_exchange(name=self.__exchange_name__, durable=True)

    @analyze_execution_time(DECLARE_QUEUE_LATENCY)
    async def declare_queue(
        self, queue_name: str = '', routing_key: str | None = None, exclusive: bool = False
    ) -> AbstractQueue:
        await self.declare_exchange()

        channel = await self.channel()
        queue = await channel.declare_queue(queue_name, exclusive=exclusive)
        exchange = await channel.get_exchange(self.__exchange_name__)

        await queue.bind(exchange=exchange, routing_key=routing_key)

        return queue

    async def consume_messages(self, queue_name: str = '', prefetch_count: int = 1) -> None:
        channel = await self.channel()
        await channel.set_qos(prefetch_count=prefetch_count)

        queue = await self.declare_queue(queue_name=queue_name, exclusive=not queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:  # type: aio_pika.Message
                async with message.process():
                    TOTAL_CONSUMER_RECEIVE_MESSAGES.inc()
                    logger.info('Consume message...')
                    await self.processing_message(message)

    @analyze_execution_time(PRODUCE_MESSAGE_LATENCY)
    async def base_produce_message(self, data: dict[Any, Any], queue: str) -> None:
        logger.info('Producing message...')

        await self.declare_exchange()
        await self.declare_queue(queue)

        channel = await self.channel()
        exchange = await channel.get_exchange(self.__exchange_name__)
        message = aio_pika.Message(msgpack.packb(data))

        await exchange.publish(message, queue)
        logger.warning('Produced message...')

    async def wait_answer_for_user(
        self,
        queue_name: str,
        user_id: int,
        success_callback: Callable[[bool], Coroutine],
        prefetch_count: int = 1,
        no_ack: bool = True,
    ) -> None:
        await self.declare_exchange()
        channel = await self.channel()
        await channel.set_qos(prefetch_count=prefetch_count)
        queue_name = f'{queue_name}.{user_id}'

        logger.info('Handler started waiting for answer in queue: %s', queue_name)

        queue = await self.declare_queue(queue_name=queue_name, exclusive=False)
        for _ in range(self.__RETRIES):

            try:
                logger.info('Try to get value from queue...')
                is_reg = await queue.get(no_ack=no_ack)
                queue_value: bool = msgpack.unpackb(is_reg.body)
                logger.debug('Got value from queue %s', queue_value)
                await success_callback(queue_value)
                break
            except QueueEmpty:
                await asyncio.sleep(1)

    @analyze_execution_time(PRODUCE_MESSAGE_LATENCY)
    async def publish_message_to_user(self, message: Any, queue_name: str) -> None:
        await self.declare_exchange()
        await self.declare_queue(queue_name)
        channel = await self.channel()
        exchange = await channel.get_exchange(self.__exchange_name__)
        pika_message = aio_pika.Message(msgpack.packb(message))
        await exchange.publish(pika_message, queue_name)
        logger.info('Message published in queue: %s', queue_name)

    @abstractmethod
    @analyze_execution_time(PROCESSING_MESSAGE_LATENCY)
    async def processing_message(self, message: Message) -> None:
        pass
