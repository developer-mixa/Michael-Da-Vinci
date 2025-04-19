from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.apps.bot.analytics.metrics import TOTAL_BOT_SEND_MESSAGES

class CalculationAnalyticsMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        result = await handler(event, data)
        TOTAL_BOT_SEND_MESSAGES.inc()
        return result