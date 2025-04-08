import logging
import msgpack
import aio_pika
from aio_pika.abc import AbstractQueue
from src.apps.consumers.base.rabbit_base import RabbitBase
from config.settings import settings
from typing import Any
from .schema.registration import RegistrationData
from src.storage.db import async_session

from sqlalchemy import insert
from ..model.models import User

logger = logging.getLogger(__name__)

class RegisterUpdatesRabbit(RabbitBase):

    async def declare_register_updates_exchange(self) -> None:
        channel = await self.channel()
        await channel.declare_exchange(name=settings.REGISTRATION_EXCHANGE_NAME, durable=True)

    async def declare_register_updates_queue(
        self,
        queue_name: str = "",
        routing_key: str = None,
        exclusive: bool = False
    ) -> AbstractQueue:
        await self.declare_register_updates_exchange()

        channel = await self.channel()
        queue = await channel.declare_queue(queue_name, exclusive=exclusive)
        exchange = await channel.get_exchange(settings.REGISTRATION_EXCHANGE_NAME)

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
                    parsed_reg_data: RegistrationData = msgpack.unpackb(message.body)
                    logger.info("Got messages %s", parsed_reg_data)
