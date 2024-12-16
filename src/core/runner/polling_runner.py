import asyncio
from src.core.runner.base.bot_runner import BotRunner
import logging

logger = logging.getLogger(__name__)

class PollingRunner(BotRunner):

    async def run(self):
        logger.info('Starting polling')

        await self._setup()
        await self._bot.delete_webhook()

        logging.error('Dependencies launched')
        await self._dp.start_polling(self._bot)