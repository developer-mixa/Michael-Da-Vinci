from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import time
from src.apps.bot.analytics.metrics import TOTAL_BOT_RPS

class CalculationRpsMiddleware(BaseMiddleware):

    def __init__(self):
        self.rps = 0
        self.last_update_time = time.monotonic()

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        current_time = time.monotonic()
        
        delta_time = current_time - self.last_update_time
        
        if delta_time > 1:
            self.rps = self.rps / delta_time
            self.last_update_time = current_time
        
        self.rps += 1

        TOTAL_BOT_RPS.set(self.rps)

        result = await handler(event, data)
        
        return result