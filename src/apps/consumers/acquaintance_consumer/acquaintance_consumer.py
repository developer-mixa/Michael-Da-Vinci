from asyncio import QueueEmpty
import logging
import msgpack
from aio_pika import Message
from sqlalchemy import select
from src.apps.consumers.acquaintance_consumer.schema.acquintance_data import BaseAcquaintanceData, MutualityData, SearchAcquaintanceData, LikeUserData
from src.apps.consumers.acquaintance_consumer.schema.responses.__main__ import AcquaintanceResponse, AcquaintanceResponseStatus, LikedResponseStatus
from src.apps.consumers.base.base_consumer import BaseConsumer
from config.settings import settings
from src.apps.consumers.common.user_data import UserData
from src.apps.consumers.model.models import User
from .data.acquaintance_repository import AcquaintanceRepository
from ..errors.errors import NonRegisteredError

from src.apps.files_storage.storage_client import images_storage


logger = logging.getLogger(__name__)

class AcquaintanceRabbit(BaseConsumer):

    __exchange_name__ = settings.ACQUAINTANCE_EXCHANGE_NAME

    def __init__(self):
        self.acquaintance_repository = AcquaintanceRepository()

    async def processing_message(self, message: Message):

        acquaintance_data: BaseAcquaintanceData = msgpack.unpackb(message.body)
        logger.info("Received message %s", acquaintance_data['action'])
        acquaintance_action = acquaintance_data['action']
        if acquaintance_action == 'search':
            await self.search_users(acquaintance_data)
        elif acquaintance_action == 'like_user':
            await self.like_user(acquaintance_data)
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
                await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.FOUND.serialize(), data=user_data), search_queue_name)
            else:
                await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.NOT_FOUND.serialize()), search_queue_name)
        except NonRegisteredError:
            await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.NON_REGISTERED.serialize()), search_queue_name)
        except BaseException as e:
            logger.error('Unexcepted exception: %s', str(e))
            await self.publish_message_to_user(AcquaintanceResponse(response=AcquaintanceResponseStatus.UNEXCEPTED_ERROR.serialize()), search_queue_name)

    async def like_user(self, acquaintance_data: LikeUserData):
        await self.declare_exchange()

        sender_id: int = acquaintance_data['user_id']
        liked_user_id: int = acquaintance_data['liked_user_id']

        try:
            is_mutual_like = await self._check_user_compability(liked_user_id, sender_id)
            if is_mutual_like:
                await self.publish_message_to_user(
                    message=AcquaintanceResponse(
                        response=LikedResponseStatus.MUTUALLY.serialize(),
                        data=MutualityData(liked_user_id=liked_user_id, sender_user_id=sender_id)
                    ),
                    queue_name=f'{settings.ACQUAINTANCE_LIKE_QUEUE_NAME}.{sender_id}'
                )
            else:
                await self._like_user(sender_id, liked_user_id)
        except BaseException as e:
            logger.error('Unexcepted exception: %s', str(e))
            await self.publish_message_to_user(
                message=AcquaintanceResponse(
                    response=LikedResponseStatus.UNEXCEPTED_ERROR.serialize(),
                    data=None
                    ),
                    queue_name=f'{settings.ACQUAINTANCE_LIKE_QUEUE_NAME}.{sender_id}'
                )

    async def _check_user_compability(self, liked_user_id, user_sender_id):
        logger.info("Checking for compatibility %s and %s", liked_user_id, user_sender_id)

        liked_user_queue_name: str = f'{settings.LIKES_QUEUE_NAME}.{liked_user_id}'
        liked_user_queue = await self.declare_queue(queue_name=liked_user_queue_name)
        while True:
            try:
                user_message = await liked_user_queue.get()
                
                user_id: int = msgpack.unpackb(user_message.body)['data']
                logger.info("Comparing %s and %s", user_id, user_sender_id)
                if user_id == user_sender_id:
                    return True
            except QueueEmpty:
                return False
    
    async def _like_user(self, sender_id: int, liked_user_id: int):
        user_likes_queue: str = f'{settings.LIKES_QUEUE_NAME}.{sender_id}'
        await self.publish_message_to_user(
            message=AcquaintanceResponse(
                response=LikedResponseStatus.LIKE_SENT.serialize(),
                data=liked_user_id
            ),
            queue_name=user_likes_queue
        )