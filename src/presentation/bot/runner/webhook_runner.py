"""Webhook bot runner."""

import logging

from config.settings import settings
from src.presentation.bot.runner.base_runner import BotRunner
from src.presentation.bot.webhook.settings import WEBHOOK_ENDPOINT

logger = logging.getLogger(__name__)


class WebhookRunner(BotRunner):
    async def run(self) -> None:
        await self._setup()
        await self._bot.set_webhook(settings.BOT_WEBHOOK_URL + WEBHOOK_ENDPOINT)

