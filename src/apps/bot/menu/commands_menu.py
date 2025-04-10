from aiogram.types import BotCommand
from src.apps.bot.commands import commands

bot_commands = [
    BotCommand(command=commands.REGISTRATION, description="Зарегистрироваться"),
    BotCommand(command=commands.ACTIVATING, description="Показывать профиль в ленте"),
    BotCommand(command=commands.DEACTIVATING, description="Не показывать профиль в ленте")
]