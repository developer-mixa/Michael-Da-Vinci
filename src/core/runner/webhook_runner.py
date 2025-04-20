import logging

from config.settings import settings
from src.apps.bot.webhook.settings import WEBHOOK_ENDPOINT
from src.core.runner.base.bot_runner import BotRunner

logger = logging.getLogger(__name__)


class WebhookRunner(BotRunner):
    async def run(self) -> None:
        await self._setup()
        await self._bot.set_webhook(settings.BOT_WEBHOOK_URL + WEBHOOK_ENDPOINT)
