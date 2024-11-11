from src.apps.consumers.register_consumer.register_updates_rabbit import RegisterUpdatesRabbit
import asyncio
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting consumer...")
    async with RegisterUpdatesRabbit() as rabbit:
        await rabbit.consume_messages(queue_name=settings.REGISTRATION_QUEUE_NAME)

if __name__ == '__main__':
    asyncio.run(main())