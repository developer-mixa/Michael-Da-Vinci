import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from fastapi import FastAPI, logger
import uvicorn
from config.settings import settings
from src.core.runner.base.bot_runner import BotRunner
from src.core.runner.polling_runner import PollingRunner
from src.core.runner.webhook_runner import WebhookRunner

from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from src.apps.api.analytics.router import router as analytics_router
from src.apps.bot.webhook.router import router as webhook_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

bot_runner: BotRunner = WebhookRunner() if settings.BOT_WEBHOOK_URL else PollingRunner()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    polling_task: asyncio.Task[None] | None = None

    wh_info = await bot_runner._bot.get_webhook_info()
    if settings.BOT_WEBHOOK_URL and wh_info.url != settings.BOT_WEBHOOK_URL:
        await bot_runner.run()
    else:
        polling_task = asyncio.create_task(bot_runner.run())

    logger.info("Finished start")
    yield

    if polling_task is not None:
        logger.info("Stopping polling...")
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info("Polling stopped")

    logger.info('Ending lifespan')

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(analytics_router)
    app.include_router(webhook_router)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app

if __name__ == "__main__":
    uvicorn.run('src.main.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)