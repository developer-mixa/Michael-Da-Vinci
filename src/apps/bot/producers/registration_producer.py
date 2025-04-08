from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit

from config.settings import settings

import logging

import aio_pika
import msgpack

from src.apps.consumers.register_consumer.schema.registration import RegistrationData

logger = logging.getLogger(__name__)

class RegistrationProducer(RegisterUpdatesRabbit):
    async def produce_message(self, registration_data: RegistrationData):
        logger.info("Producing message %s", registration_data)

        await self.declare_register_updates_exchange()
        await self.declare_register_updates_queue(settings.REGISTRATION_QUEUE_NAME)

        channel = await self.channel()
        exchange = await channel.get_exchange(settings.REGISTRATION_EXCHANGE_NAME)
        message = aio_pika.Message(msgpack.packb(registration_data))

        await exchange.publish(message, settings.REGISTRATION_QUEUE_NAME)
        logger.warning("Produced message %s", message.body)