import logging

from src.core.runner.base.bot_runner import BotRunner

logger = logging.getLogger(__name__)


class PollingRunner(BotRunner):

    async def run(self):
        logger.info('Starting polling')

        await self._setup()
        await self._bot.delete_webhook()

        logger.error('Dependencies launched')
        await self._dp.start_polling(self._bot)
