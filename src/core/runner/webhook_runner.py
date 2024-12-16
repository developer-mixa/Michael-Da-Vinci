import logging

from config.settings import settings
from src.core.runner.base.bot_runner import BotRunner

import asyncio

logger = logging.getLogger(__name__)

class WebhookRunner(BotRunner):
    async def run(self):
        await self._setup()
        await self._bot.set_webhook(settings.BOT_WEBHOOK_URL)