import asyncio
from asyncio import Task
from typing import Any

from aiogram.methods.base import TelegramMethod
from starlette.requests import Request

from src.apps.bot.webhook.settings import WEBHOOK_ENDPOINT

from .router import router
from src.apps.bot.bot import get_dp, get_bot

background_tasks: set[Task[TelegramMethod[Any] | None]] = set()

@router.post(WEBHOOK_ENDPOINT)
async def webhook(request: Request) -> None:
    bot, dp = get_bot(), get_dp()

    update = await request.json()

    task: Task[TelegramMethod[Any] | None] = asyncio.create_task(dp.feed_webhook_update(bot, update))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)