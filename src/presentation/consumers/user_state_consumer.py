"""Presentation consumer: User state — processes profile update messages."""

import logging

import msgpack
from aio_pika import Message

from config.settings import settings
from src.application.dto.update_user import UpdateUserInput
from src.application.use_cases.update_user_state import UpdateUserStateUseCase
from src.infrastructure.metrics.consumer_metrics import PROCESSING_MESSAGE_LATENCY
from src.infrastructure.rabbit.base import BaseConsumer

logger = logging.getLogger(__name__)


class UserStateConsumer(BaseConsumer):

    __exchange_name__ = settings.UPDATE_USER_EXCHANGE_NAME

    def __init__(self, rabbit_url: str, use_case: UpdateUserStateUseCase) -> None:
        super().__init__(rabbit_url)
        self._use_case = use_case

    async def processing_message(self, message: Message) -> None:
        with PROCESSING_MESSAGE_LATENCY.time():
            parsed = msgpack.unpackb(message.body)
            logger.info('Received update message: %s', parsed)

            user_id = parsed['user_id']
            queue_name = f'{settings.UPDATE_USER_QUEUE_NAME}.{user_id}'

            data = UpdateUserInput(
                user_id=user_id,
                name=parsed.get('name'),
                age=parsed.get('age'),
                description=parsed.get('description'),
                status=parsed.get('status'),
                image=parsed.get('image'),
            )

            try:
                success = await self._use_case.execute(data)
                await self.publish_message_to_user(success, queue_name)
            except Exception as e:
                logger.exception('Error processing update: %s', e)
                await self.publish_message_to_user(False, queue_name)

