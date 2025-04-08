from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit
import asyncio
from aio_pika import Message
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting consumer...")
    async with RegisterUpdatesRabbit() as rabbit:
        await rabbit.consume_messages(handle_message, queue_name=settings.REGISTRATION_QUEUE_NAME)

def handle_message(message: Message):
    logger.info("Got message: %s", message.body)
    ...

if __name__ == '__main__':
    asyncio.run(main())