import asyncio

from src.apps.consumers.base.base_consumer import BaseConsumer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class ConsumerRunner:
    def __init__(self, consumer: BaseConsumer, queue_name: str):
        self.__consumer = consumer
        self.__queue_name = queue_name

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        logger.info("Starting consumer...")
        async with self.__consumer as rabbit:
            await rabbit.consume_messages(queue_name=self.__queue_name)