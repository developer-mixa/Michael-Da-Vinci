import logging
from config.settings import settings
from src.core.runner.base.bot_runner import BotRunner
from src.core.runner.polling_runner import PollingRunner
from src.core.runner.webhook_runner import WebhookRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    bot_runner: BotRunner = WebhookRunner() if settings.BOT_WEBHOOK_URL else PollingRunner()
    bot_runner.run()