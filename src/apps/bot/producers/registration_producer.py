import asyncio
from typing import Callable, Coroutine

from aio_pika.exceptions import QueueEmpty

from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit

from config.settings import settings

import logging

import aio_pika
import msgpack

from src.apps.consumers.register_consumer.schema.registration import RegistrationData

logger = logging.getLogger(__name__)

class RegistrationProducer(RegisterUpdatesRabbit):

    __RETRIES = 5

    async def produce_message(self, registration_data: RegistrationData):
        logger.info("Producing message %s", registration_data)

        await self.declare_register_updates_exchange()
        await self.declare_register_updates_queue(settings.REGISTRATION_QUEUE_NAME)

        channel = await self.channel()
        exchange = await channel.get_exchange(settings.REGISTRATION_EXCHANGE_NAME)
        message = aio_pika.Message(msgpack.packb(registration_data))

        await exchange.publish(message, settings.REGISTRATION_QUEUE_NAME)
        logger.warning("Produced message %s", message.body)

    async def wait_register_answer(self, user_id, register_callback: Callable[[bool], Coroutine]):
        channel = await self.channel()
        await channel.set_qos(prefetch_count=1)
        queue_name = f'{settings.REGISTRATION_QUEUE_NAME}.{user_id}'

        logger.info("Registration handler started waiting for answer...")

        queue = await self.declare_register_updates_queue(queue_name=queue_name, exclusive=not queue_name)
        for _ in range(self.__RETRIES):
            try:
                logger.info("Try to get value from queue...")
                is_reg = await queue.get()
                parsed_is_reg: bool = msgpack.unpackb(is_reg.body)
                logger.info("Got value from queue: %s", parsed_is_reg)
                await register_callback(parsed_is_reg)
                break
            except QueueEmpty:
                await asyncio.sleep(1)
