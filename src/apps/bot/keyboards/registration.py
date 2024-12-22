from aiogram.types import KeyboardButton

from .texts import BOY, GIRL, OK as OK_TEXT, SEND_LOCATION
from .utils import create_single_button, create_single_row_buttons

OK = create_single_button(OK_TEXT)
GENDERS = create_single_row_buttons([KeyboardButton(text=GIRL), KeyboardButton(text=BOY)])
LOCATION = create_single_button(SEND_LOCATION)
