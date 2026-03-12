"""Pure domain validator for user name (no Telegram dependency)."""

from src.domain import exceptions as e

MAX_NAME_LEN = 15
MIN_NAME_LEN = 2


def validate_name(name: str) -> str:
    """Validate and return the name. Raises domain ValidationError subclasses."""
    if not name.isalpha():
        raise e.NameCanContainLettersError
    if len(name) >= MAX_NAME_LEN:
        raise e.TooLongNameError
    if len(name) < MIN_NAME_LEN:
        raise e.TooShortNameError
    if ' ' in name or '\n' in name:
        raise e.NameCannotContainSpacesError
    if name[0].islower():
        raise e.NameBeginCannotBeLowercaseError
    return name

