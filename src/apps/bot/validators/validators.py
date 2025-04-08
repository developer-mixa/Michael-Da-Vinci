from . import errors as e
from .base.base_validator import BaseTgValidator
from datetime import datetime
from .utils import AGE_FORMAT

MAX_NAME_LEN = 15
MIN_NAME_LEN = 2

MIN_AGE = 0
MAX_AGE = 200

class NameValidator(BaseTgValidator):
    def _do_validate(self, message: str):
        if not message.isalpha():
            raise e.NameCanContainLettersError
        if len(message) >= MAX_NAME_LEN:
            raise e.TooLongNameError
        if len(message) < MIN_NAME_LEN:
            raise e.TooShortNameError
        if message.count(' ') > 0 or message.count('\n') > 0:
            raise e.NameCannotContainSpacesError
        if message[0].islower():
            raise e.NameBeginCannotBeLowercaseError

class AgeValidator(BaseTgValidator):
    def _do_validate(self, message: str):
        try:
            datetime.strptime(message, AGE_FORMAT).date()
        except Exception:
            raise e.WrongAgeFormatError