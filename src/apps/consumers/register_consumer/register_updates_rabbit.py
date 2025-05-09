import io
import logging

import msgpack
from aio_pika import Message
from sqlalchemy.exc import IntegrityError

from config.settings import settings
from src.apps.consumers.base.base_consumer import BaseConsumer
from src.apps.consumers.common.analytics import PROCESSING_MESSAGE_LATENCY
from src.apps.files_storage.storage_client import images_storage
from src.core.utils.time import analyze_execution_time
from src.storage.db import async_session

from ..mappers.user_mapper import user_from_reg_data
from .schema.registration import RegistrationData

import base64

logger = logging.getLogger(__name__)


class RegisterUpdatesRabbit(BaseConsumer):

    __exchange_name__ = settings.REGISTRATION_EXCHANGE_NAME

    @analyze_execution_time(PROCESSING_MESSAGE_LATENCY)
    async def processing_message(self, message: Message) -> None:
        try:
            parsed_reg_data: RegistrationData = msgpack.unpackb(message.body)
            logger.info('Received message %s', parsed_reg_data)
            user = user_from_reg_data(parsed_reg_data)
            queue_name = f'{settings.REGISTRATION_QUEUE_NAME}.{parsed_reg_data["user_id"]}'

            async with async_session() as db:
                logger.info('Upload image to minio...')
                image_bytes = base64.b64decode(parsed_reg_data['image'])
                images_storage.upload_file(str(user.telegram_id), io.BytesIO(image_bytes))
                db.add(user)
                await db.commit()
                await self.publish_message_to_user(True, queue_name)
        except IntegrityError:
            logger.info('This user with this data is already registered: %s', parsed_reg_data)
            await self.publish_message_to_user(False, queue_name)
        except Exception as e:
            logger.info('Something went wrong... %s', str(e))
            await self.publish_message_to_user(False, queue_name)
