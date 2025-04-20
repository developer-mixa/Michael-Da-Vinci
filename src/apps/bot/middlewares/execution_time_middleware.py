from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import time
from src.apps.bot.analytics.metrics import BOT_EXECUTION_LATENCY

class CalculationExecutionTimeMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):

        start = time.monotonic()

        result = await handler(event, data)

        end = time.monotonic()

        BOT_EXECUTION_LATENCY.observe(end - start)
        
        return result