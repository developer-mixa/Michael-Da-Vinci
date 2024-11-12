import logging

import aio_pika
import msgpack
from aio_pika import Message
from aio_pika.abc import AbstractExchange

from src.apps.consumers.base.base_consumer import BaseConsumer
from config.settings import settings
from .schema.registration import RegistrationData
from src.storage.db import async_session
from ..mappers.user_mapper import user_from_reg_data
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class RegisterUpdatesRabbit(BaseConsumer):

    __exchange_name__ = settings.REGISTRATION_EXCHANGE_NAME

    async def processing_message(self, message: Message):
        parsed_reg_data: RegistrationData = msgpack.unpackb(message.body)
        logger.info("Got message %s", parsed_reg_data)
        user = user_from_reg_data(parsed_reg_data)
        channel = await self.channel()
        exchange = await channel.get_exchange(settings.REGISTRATION_EXCHANGE_NAME)
        queue_name = f'{settings.REGISTRATION_QUEUE_NAME}.{parsed_reg_data["user_id"]}'

        try:
            async with async_session() as db:
                db.add(user)
                await db.commit()
                await self.__publish_message_to_user(exchange, True, queue_name)
        except IntegrityError:
            logger.info("This user with this data is already registered: %s", parsed_reg_data)
            await self.__publish_message_to_user(exchange, False, queue_name)

    @staticmethod
    async def __publish_message_to_user(exchange: AbstractExchange, is_success_register: bool, queue_name: str):
        message = aio_pika.Message(msgpack.packb(is_success_register))
        await exchange.publish(message, queue_name)