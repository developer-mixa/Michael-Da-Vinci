from src.apps.bot.messages.flood import NO_COMMAND_FOUND
from .router import router
from aiogram.types import Message

@router.message()
async def handle_flood(message: Message):
    await message.answer(NO_COMMAND_FOUND)