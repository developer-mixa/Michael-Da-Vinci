"""Infrastructure: ConsumerRunner for running RabbitMQ consumers."""

import asyncio
import logging

from src.infrastructure.rabbit.base import BaseConsumer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConsumerRunner:
    def __init__(self, consumer: BaseConsumer, queue_name: str) -> None:
        self._consumer = consumer
        self._queue_name = queue_name

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        logger.info('Starting consumer...')
        async with self._consumer as rabbit:
            await rabbit.consume_messages(queue_name=self._queue_name)

