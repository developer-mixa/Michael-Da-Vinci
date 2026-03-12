"""Bot handler: Catch-all flood messages."""

from aiogram import Router
from aiogram.types import Message

from src.presentation.bot.messages.flood import NO_COMMAND_FOUND

router = Router()


@router.message()
async def handle_flood(message: Message) -> None:
    await message.answer(NO_COMMAND_FOUND)

