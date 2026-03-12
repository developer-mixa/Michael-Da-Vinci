"""Infrastructure: RabbitMQ base connection management."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine

import aio_pika
import msgpack
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection
from aio_pika.channel import Channel
from aio_pika.connection import Connection
from aio_pika.exceptions import QueueEmpty
from aio_pika.pool import Pool

logger = logging.getLogger(__name__)


class RabbitException(Exception):
    pass


class RabbitBase:
    def __init__(self, rabbit_url: str) -> None:
        self._rabbit_url = rabbit_url
        self._connection_pool: Pool[Connection] | None = None
        self._channel_pool: Pool[Channel] | None = None

    async def _get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(self._rabbit_url)

    async def _get_channel(self) -> AbstractChannel:
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()

    async def channel(self) -> Channel:
        if self._channel_pool is None:
            raise RabbitException('Please use context manager for Rabbit helper.')
        async with self._channel_pool.acquire() as channel:
            return channel

    async def __aenter__(self):
        self._connection_pool = Pool(self._get_connection, max_size=2)
        self._channel_pool = Pool(self._get_channel, max_size=10)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._channel_pool and not self._channel_pool.is_closed:
            await self._channel_pool.close()
        if self._connection_pool and not self._connection_pool.is_closed:
            await self._connection_pool.close()


class BaseConsumer(RabbitBase, ABC):
    """Base class for RabbitMQ consumers with exchange/queue management."""

    __exchange_name__: str
    __RETRIES = 45

    async def declare_exchange(self) -> None:
        channel = await self.channel()
        await channel.declare_exchange(name=self.__exchange_name__, durable=True)

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
            async for message in queue_iter:
                async with message.process():
                    logger.info('Consume message...')
                    await self.processing_message(message)

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
                is_reg = await queue.get(no_ack=no_ack)
                queue_value = msgpack.unpackb(is_reg.body)
                await success_callback(queue_value)
                break
            except QueueEmpty:
                await asyncio.sleep(1)

    async def publish_message_to_user(self, message: Any, queue_name: str) -> None:
        await self.declare_exchange()
        await self.declare_queue(queue_name)
        channel = await self.channel()
        exchange = await channel.get_exchange(self.__exchange_name__)
        pika_message = aio_pika.Message(msgpack.packb(message))
        await exchange.publish(pika_message, queue_name)

    @abstractmethod
    async def processing_message(self, message: Message) -> None:
        pass

