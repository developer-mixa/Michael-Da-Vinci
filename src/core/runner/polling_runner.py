import asyncio

from aiogram.fsm.storage.memory import MemoryStorage

from src.apps.bot.bot import setup_dp, setup_bot
from src.core.runner.base.bot_runner import BotRunner
import logging
from aiogram import Bot, Dispatcher
from config.settings import settings
from src.apps.bot.handlers.registration.router import router as registration_router

logger = logging.getLogger(__name__)

class PollingRunner(BotRunner):

    def __init__(self):
        self.__dp = Dispatcher(storage=MemoryStorage())
        setup_dp(self.__dp)

        self.__bot = Bot(token=settings.BOT_TOKEN)
        setup_bot(self.__bot)

    def run(self):
        asyncio.run(self.__run())

    async def __run(self):
        logger.info('Starting polling')

        self.__dp.include_router(registration_router)
        await self.__bot.delete_webhook()

        logging.error('Dependencies launched')
        await self.__dp.start_polling(self.__bot)
