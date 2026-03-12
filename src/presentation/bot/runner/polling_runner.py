"""Polling bot runner."""

import logging

from src.presentation.bot.runner.base_runner import BotRunner

logger = logging.getLogger(__name__)


class PollingRunner(BotRunner):

    async def run(self) -> None:
        logger.info('Starting polling')
        await self._setup()
        await self._bot.delete_webhook()
        logger.info('Dependencies launched')
        await self._dp.start_polling(self._bot)

