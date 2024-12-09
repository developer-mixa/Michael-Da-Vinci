from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.apps.bot.commands.commands import CALLBACK_UPDATE_PREFIX, CALLBACK_BACK_MENU

FORM_FIELDS = [
    ['Имя', 'name'],
    ['Описание', 'description'],
    ['Местоположение', 'location'],
    ['Изображение', 'image']
]

def get_button_name_by_key(key: str) -> str:
    for form in FORM_FIELDS:
        if form[1] == key:
            return form[0].lower()
    return ''


BACK_TO_MENU = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data=CALLBACK_BACK_MENU)]])

async def inline_user_state_fields() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for field in FORM_FIELDS:
        keyboard.add(InlineKeyboardButton(text=field[0], callback_data=CALLBACK_UPDATE_PREFIX + field[1]))
    return keyboard.adjust(2).as_markup()