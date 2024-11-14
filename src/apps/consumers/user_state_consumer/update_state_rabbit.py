import logging

import aio_pika
import msgpack
from aio_pika import Message
from aio_pika.abc import AbstractExchange
from sqlalchemy import select

from config.settings import settings
from src.apps.consumers.base.base_consumer import BaseConsumer
from src.apps.consumers.user_state_consumer.schema.update_user_state import UpdateUserData
from src.storage.db import async_session
from ..errors.errors import NonRegisteredError
from ..model.models import User

logger = logging.getLogger(__name__)

class UpdateStateRabbit(BaseConsumer):

    __exchange_name__ = settings.UPDATE_USER_EXCHANGE_NAME

    async def processing_message(self, message: Message):
        parsed_user_data: UpdateUserData = msgpack.unpackb(message.body)
        logger.info("Received message: %s", parsed_user_data)

        channel = await self.channel()
        exchange = await channel.get_exchange(settings.UPDATE_USER_EXCHANGE_NAME)
        queue_name = f'{settings.UPDATE_USER_QUEUE_NAME}.{parsed_user_data["user_id"]}'

        try:
            async with async_session() as db:
                user: User = await db.scalar(select(User).where(User.telegram_id == parsed_user_data.get('user_id')))
                if not user:
                    raise NonRegisteredError
                for param, value in parsed_user_data.items():
                    if value and param != 'user_id':
                        setattr(user, param, value)
                await db.commit()
                await self.__publish_message_to_user(exchange, True, queue_name)
        except NonRegisteredError:
            await self.__publish_message_to_user(exchange, False, queue_name)
            pass

    @staticmethod
    async def __publish_message_to_user(exchange: AbstractExchange, is_success_register: bool, queue_name: str):
        message = aio_pika.Message(msgpack.packb(is_success_register))
        await exchange.publish(message, queue_name)