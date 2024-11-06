import logging.config

import aio_pika
import msgpack

from src.apps.consumer.handlers.registration import handle_event_registration
from src.apps.consumer.logger import LOGGING_CONFIG, logger, correlation_id_ctx
from src.apps.consumer.schema.registration import RegistrationData
from src.storage.rabbit import channel_pool
from src.apps.consumer.actions import REGISTER_USER

import asyncio

async def main() -> None:
    #logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Starting consumer...')


    queue_name = "user_messages"
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel

        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter: # type: aio_pika.Message
                async with message.process():
                    correlation_id_ctx.set(message.correlation_id)
                    logger.info("Message ...")

                    body: RegistrationData = msgpack.unpackb(message.body)
                    if body['event'] == REGISTER_USER:
                        await handle_event_registration(body)

if __name__ == "__main__":
    asyncio.run(main())