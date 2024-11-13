import logging

import msgpack
from aio_pika import Message
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

        try:
            async with async_session() as db:
                user: User = await db.scalar(select(User).where(User.telegram_id == parsed_user_data.get('user_id')))
                if not user:
                    raise NonRegisteredError
                for param, value in parsed_user_data.items():
                    if value and param != 'user_id':
                        setattr(user, param, value)
                await db.commit()
        except NonRegisteredError:
            # Tell user so that he will register
            pass