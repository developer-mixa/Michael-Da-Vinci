import asyncio

from aiogram.types import Update
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.server.bot.router import router
from src.tasks import background_tasks
from src.bot.bot import get_dp, get_bot


@router.post("/home")
async def home_post(
    request: Request,
    # session: AsyncSession = Depends(get_db),
) -> JSONResponse:
    a = 1
    data = await request.json()
    update = Update(**data)
    dp = get_dp()

    task = asyncio.create_task(dp.feed_webhook_update(get_bot(), update))
    background_tasks.add(task)

    return ORJSONResponse({"message": "Hello"})