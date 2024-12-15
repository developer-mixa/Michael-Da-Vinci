import uvicorn
import logging

from fastapi import FastAPI
from config.settings import settings
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins
from src.core.runner.base.bot_runner import BotRunner

import asyncio

logger = logging.getLogger(__name__)

class WebhookRunner(BotRunner):
    def run(self):
        asyncio.run(self.__run())

    async def __run(self):
        await self._setup()
        await self._bot.set_webhook(settings.BOT_WEBHOOK_URL)
        uvicorn.run('src.core.runner.webhook_runner:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app