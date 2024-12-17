from abc import ABC, abstractmethod

from aiogram import Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from src.apps.bot.bot import setup_dp, setup_bot
from aiogram import Bot, Dispatcher
from config.settings import settings
from src.apps.bot.handlers.registration.router import router as registration_router
from src.apps.bot.handlers.user_state.router import router as user_state_router
from src.apps.bot.handlers.acquaintance.router import router as acquaintance_router
from src.apps.bot.handlers.flood.router import router as flood_router
from src.apps.bot.middlewares.calculation_analytics import CalculationAnalyticsMiddleware
from src.apps.bot.middlewares.rps import CalculationRpsMiddleware
from src.apps.bot.menu.commands_menu import bot_commands

class BotRunner(ABC):

    def __init__(self):
        self._dp = Dispatcher(storage=MemoryStorage())
        setup_dp(self._dp)

        self._bot = Bot(token=settings.BOT_TOKEN)
        setup_bot(self._bot)

    @abstractmethod
    async def run(self):
        pass

    async def _setup(self):
        await self._bot.set_my_commands(bot_commands)

        self._dp.include_router(registration_router)
        self._dp.include_router(user_state_router)
        self._dp.include_router(acquaintance_router)
        self._dp.include_router(flood_router)
        self._dp.update.outer_middleware(CalculationAnalyticsMiddleware())
        self._dp.update.outer_middleware(CalculationRpsMiddleware())