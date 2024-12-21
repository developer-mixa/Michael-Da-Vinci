from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

OK = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ok')]], resize_keyboard=True)


def create_single_row_buttons(buttons: list[KeyboardButton]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)


def create_single_button(text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text)]], resize_keyboard=True)
