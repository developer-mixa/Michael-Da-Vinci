import logging
import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractQueue
from src.apps.consumers.base.rabbit_base import RabbitBase

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseConsumer(RabbitBase, ABC):

    __exchange_name__: str

    async def declare_register_updates_exchange(self) -> None:
        channel = await self.channel()
        await channel.declare_exchange(name=self.__exchange_name__, durable=True)

    async def declare_register_updates_queue(
        self,
        queue_name: str = "",
        routing_key: str = None,
        exclusive: bool = False
    ) -> AbstractQueue:
        await self.declare_register_updates_exchange()

        channel = await self.channel()
        queue = await channel.declare_queue(queue_name, exclusive=exclusive)
        exchange = await channel.get_exchange(self.__exchange_name__)

        await queue.bind(exchange=exchange, routing_key=routing_key)

        return queue

    async def consume_messages(
            self,
            queue_name: str = "",
            prefetch_count: int = 1) -> None:
        channel = await self.channel()
        await channel.set_qos(prefetch_count=prefetch_count)

        queue = await self.declare_register_updates_queue(queue_name=queue_name, exclusive=not queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter: # type: aio_pika.Message
                async with message.process():
                    logger.info("Consume message...")
                    await self.processing_message(message)

    @abstractmethod
    async def processing_message(self, message: Message):
        pass