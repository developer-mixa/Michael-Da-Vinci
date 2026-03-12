from aiogram.types import KeyboardButton

from src.presentation.bot.emoji import DISLIKE, LIKE, STOP

from .utils import create_single_row_buttons

CHOISES = create_single_row_buttons(
    [KeyboardButton(text=LIKE), KeyboardButton(text=DISLIKE), KeyboardButton(text=STOP)]
)

