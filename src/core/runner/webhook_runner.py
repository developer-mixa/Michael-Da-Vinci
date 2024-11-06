import uvicorn
import logging

from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from src.apps.bot.bot import setup_dp, setup_bot
from config.settings import settings
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins
from src.core.runner.base.bot_runner import BotRunner

logger = logging.getLogger(__name__)

class WebhookRunner(BotRunner):
    def run(self):
        uvicorn.run('src.core.runner.webhook_runner:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)


async def lifespan(app: FastAPI) -> None:

    logger.info('Starting lifespan')

    dp = Dispatcher()
    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)

    await bot.set_webhook(settings.BOT_WEBHOOK_URL)

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app