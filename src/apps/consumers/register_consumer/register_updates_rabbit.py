import logging
import msgpack
from aio_pika import Message
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
        try:
            async with async_session() as db:
                db.add(user)
                await db.commit()
        except IntegrityError:
            logger.info("This user with this data is already registered: %s", parsed_reg_data)