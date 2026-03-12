"""Pure domain validator for date of birth (no Telegram dependency)."""

from datetime import date, datetime

from src.domain.exceptions import WrongAgeFormatError

AGE_FORMAT = '%Y-%m-%d'


def validate_date_of_birth(date_string: str) -> date:
    """Parse and validate date of birth string. Returns date or raises WrongAgeFormatError."""
    try:
        return datetime.strptime(date_string, AGE_FORMAT).date()
    except Exception:
        raise WrongAgeFormatError

