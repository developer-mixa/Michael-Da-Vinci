from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .utils import create_single_button, create_single_row_buttons
from .texts import OK, GIRL, BOY, SEND_LOCATION

OK = create_single_button(OK)
GENDERS = create_single_row_buttons([KeyboardButton(text=GIRL), KeyboardButton(text=BOY)])
LOCATION = create_single_button(SEND_LOCATION)