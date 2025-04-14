import enum
import logging
from typing import Any, TypedDict

import msgpack
from aio_pika import Message
from sqlalchemy import select
from src.apps.consumers.acquaintance_consumer.schema.acquintance_data import BaseAcquaintanceData, SearchAcquaintanceData
from src.apps.consumers.acquaintance_consumer.schema.responses.__main__ import AcquaintanceResponse, AcquaintanceResponseStatus
from src.apps.consumers.base.base_consumer import BaseConsumer
from config.settings import settings
from src.apps.consumers.common.user_data import UserData
from src.apps.consumers.model.models import User
from .data.acquaintance_repository import AcquaintanceRepository
from ..errors.errors import NonRegisteredError
from src.storage.db import async_session

from src.apps.files_storage.storage_client import images_storage


logger = logging.getLogger(__name__)

class AcquaintanceRabbit(BaseConsumer):

    __exchange_name__ = settings.ACQUAINTANCE_EXCHANGE_NAME

    def __init__(self):
        self.acquaintance_repository = AcquaintanceRepository()

    async def processing_message(self, message: Message):

        acquaintance_data: BaseAcquaintanceData = msgpack.unpackb(message.body)
        logger.info("Received message %s", acquaintance_data)
        acquaintance_action = acquaintance_data['action']
        if acquaintance_action == 'search':
            await self.search_users(acquaintance_data)
        elif acquaintance_action == 'like_user':
            await self.like_user()
        else:
            # Exception
            pass
    
    async def search_users(self, acquaintance_data: SearchAcquaintanceData):
        search_queue_name: str = f'{settings.ACQUAINTANCE_QUEUE_NAME}.{acquaintance_data["user_id"]}'
        try:
            found_user: User = await self.acquaintance_repository.get_random_acquaintance(acquaintance_data['user_id'])
            found_user_image = images_storage.get_file(str(found_user.telegram_id))
            if found_user:
                user_data = UserData.from_db_user(found_user, found_user_image)
                await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.FOUND_USERS.serialize(), data=user_data), search_queue_name)
            else:
                await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.NOT_FOUND_USERS.serialize()), search_queue_name)
        except NonRegisteredError:
            await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.NON_REGISTERED.serialize()), search_queue_name)
        except BaseException as e:
            logger.error('Unexcepted exception: %s', str(e))
            await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.UNEXCEPTED_ERROR.serialize()), search_queue_name)

    async def like_user(self):
        pass