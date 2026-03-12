"""Presentation consumer: Acquaintance — processes search and like messages."""

import logging
from asyncio import QueueEmpty

import msgpack
from aio_pika import Message

from config.settings import settings
from src.application.dto.acquaintance import AcquaintanceStatus, CandidateData, LikeResult, LikeStatus, SearchResult
from src.application.use_cases.like_user import LikeUserUseCase
from src.application.use_cases.search_acquaintance import SearchAcquaintanceUseCase
from src.infrastructure.metrics.consumer_metrics import PROCESSING_MESSAGE_LATENCY
from src.infrastructure.rabbit.base import BaseConsumer

logger = logging.getLogger(__name__)

SEARCH_ACTION = 'search'
LIKE_ACTION = 'like_user'


class AcquaintanceConsumer(BaseConsumer):

    __exchange_name__ = settings.ACQUAINTANCE_EXCHANGE_NAME

    def __init__(
        self,
        rabbit_url: str,
        search_use_case: SearchAcquaintanceUseCase,
        like_use_case: LikeUserUseCase,
    ) -> None:
        super().__init__(rabbit_url)
        self._search_use_case = search_use_case
        self._like_use_case = like_use_case

    async def processing_message(self, message: Message) -> None:
        with PROCESSING_MESSAGE_LATENCY.time():
            data = msgpack.unpackb(message.body)
            action = data['action']
            logger.info('Received acquaintance message: action=%s', action)

            if action == SEARCH_ACTION:
                await self._handle_search(data)
            elif action == LIKE_ACTION:
                await self._handle_like(data)

    async def _handle_search(self, data: dict) -> None:
        user_id = data['user_id']
        queue_name = f'{settings.ACQUAINTANCE_QUEUE_NAME}.{user_id}'

        result: SearchResult = await self._search_use_case.execute(user_id)

        if result.status == AcquaintanceStatus.FOUND and result.candidate:
            c = result.candidate
            response = {
                'response': AcquaintanceStatus.FOUND.value,
                'data': {
                    'user_id': c.user_id,
                    'name': c.name,
                    'age': c.age,
                    'gender': c.gender,
                    'description': c.description,
                    'image': c.image,
                },
            }
        else:
            response = {'response': result.status.value, 'data': None}

        await self.publish_message_to_user(response, queue_name)

    async def _handle_like(self, data: dict) -> None:
        sender_id = data['user_id']
        liked_user_id = data['liked_user_id']

        # Check mutuality using the likes queue pattern (preserved from original)
        try:
            is_mutual = await self._check_mutuality(liked_user_id, sender_id)
            if is_mutual:
                await self.publish_message_to_user(
                    message={
                        'response': LikeStatus.MUTUALLY.value,
                        'data': {'liked_user_id': liked_user_id, 'sender_user_id': sender_id},
                    },
                    queue_name=f'{settings.ACQUAINTANCE_LIKE_QUEUE_NAME}.{sender_id}',
                )
            else:
                # Use the use case to record the like
                result: LikeResult = await self._like_use_case.execute(sender_id, liked_user_id)

                # Publish liked_user_id to sender's likes queue for future mutuality checks
                await self.publish_message_to_user(
                    message=liked_user_id,
                    queue_name=f'{settings.LIKES_QUEUE_NAME}.{sender_id}',
                )
                await self.publish_message_to_user(
                    message={'response': LikeStatus.LIKE_SENT.value},
                    queue_name=f'{settings.ACQUAINTANCE_LIKE_QUEUE_NAME}.{sender_id}',
                )
        except Exception as e:
            logger.exception('Error processing like: %s', e)
            await self.publish_message_to_user(
                message={'response': LikeStatus.UNEXPECTED_ERROR.value, 'data': None},
                queue_name=f'{settings.ACQUAINTANCE_LIKE_QUEUE_NAME}.{sender_id}',
            )

    async def _check_mutuality(self, liked_user_id: int, sender_id: int) -> bool:
        """Check if liked_user already liked the sender (by scanning their likes queue)."""
        logger.info('Checking mutuality between %s and %s', liked_user_id, sender_id)
        queue_name = f'{settings.LIKES_QUEUE_NAME}.{liked_user_id}'
        queue = await self.declare_queue(queue_name=queue_name)
        while True:
            try:
                user_message = await queue.get()
                uid = msgpack.unpackb(user_message.body)
                logger.info('Comparing %s and %s', uid, sender_id)
                if uid == sender_id:
                    await user_message.ack()
                    return True
            except QueueEmpty:
                return False

