"""Presentation consumer: Registration — processes registration messages from the queue."""

import base64
import io
import logging

import msgpack
from aio_pika import Message

from config.settings import settings
from src.application.dto.registration import RegistrationInput
from src.application.use_cases.register_user import RegisterUserUseCase
from src.infrastructure.metrics.consumer_metrics import PROCESSING_MESSAGE_LATENCY
from src.infrastructure.rabbit.base import BaseConsumer

logger = logging.getLogger(__name__)


class RegistrationConsumer(BaseConsumer):

    __exchange_name__ = settings.REGISTRATION_EXCHANGE_NAME

    def __init__(self, rabbit_url: str, use_case: RegisterUserUseCase) -> None:
        super().__init__(rabbit_url)
        self._use_case = use_case

    async def processing_message(self, message: Message) -> None:
        with PROCESSING_MESSAGE_LATENCY.time():
            parsed = msgpack.unpackb(message.body)
            logger.info('Received registration message: %s', parsed)

            queue_name = f'{settings.REGISTRATION_QUEUE_NAME}.{parsed["user_id"]}'

            data = RegistrationInput(
                user_id=parsed['user_id'],
                name=parsed.get('name', ''),
                age=parsed.get('age', ''),
                gender=parsed.get('gender', ''),
                description=parsed.get('description', ''),
                image_base64=parsed.get('image', ''),
                accept_privacy_policy=parsed.get('accept_privacy_policy', ''),
            )

            try:
                success = await self._use_case.execute(data)
                await self.publish_message_to_user(success, queue_name)
            except Exception as e:
                logger.exception('Error processing registration: %s', e)
                await self.publish_message_to_user(False, queue_name)

