import asyncio
import uvicorn
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.apps.bot.handlers.registration.router import router as registration_router
from src.apps.users.router import router as users_router
from config.settings import settings
from src.apps.bot.bot import setup_bot, setup_dp
from src.tasks import background_tasks
from fastapi import FastAPI
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins
from aiogram.fsm.storage.redis import RedisStorage
from src.storage.redis import setup_redis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI) -> None: # type: ignore

    logger.info('Starting lifespan')

    dp = Dispatcher()
    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)

    temp = await bot.get_webhook_info()
    await bot.set_webhook(settings.BOT_WEBHOOK_URL)
    logger.info('Finished start')
    yield
    while background_tasks:
        await asyncio.sleep(0)

    logger.info('Ending lifespan')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    app.include_router(users_router)
    return app

async def start_polling():
    logger.info('Starting polling')
    redis = setup_redis()
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=MemoryStorage())

    setup_dp(dp)
    bot = Bot(token=settings.BOT_TOKEN)
    setup_bot(bot)

    dp.include_router(registration_router)
    await bot.delete_webhook()

    logging.error('Dependencies launched')
    await dp.start_polling(bot)

def web_hook():
    pass

if __name__ == "__main__":
    if settings.BOT_WEBHOOK_URL:
        uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    else:
        asyncio.run(start_polling())