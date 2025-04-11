from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.apps.bot.commands.commands import CALLBACK_UPDATE, CALLBACK_BACK_MENU

form_fields = [
    ['Имя', 'name'],
    ['Описание', 'description'],
    ['Местоположение', 'location'],
    ['Изображение', 'image']
]

BACK_TO_MENU = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data=CALLBACK_BACK_MENU)]])

async def inline_user_state_fields() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for field in form_fields:
        keyboard.add(InlineKeyboardButton(text=field[0], callback_data=CALLBACK_UPDATE))
    return keyboard.adjust(2).as_markup()