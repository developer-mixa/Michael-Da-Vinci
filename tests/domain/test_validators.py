"""Tests for domain validators (pure, no Telegram deps)."""

import pytest

from src.domain.exceptions import (
    NameBeginCannotBeLowercaseError,
    NameCanContainLettersError,
    NameCannotContainSpacesError,
    TooLongNameError,
    TooShortNameError,
    WrongAgeFormatError,
)
from src.domain.validators.name_validator import validate_name
from src.domain.validators.age_validator import validate_date_of_birth


class TestNameValidator:

    def test_valid_name(self):
        assert validate_name("Михаил") == "Михаил"

    def test_name_with_digits(self):
        with pytest.raises(NameCanContainLettersError):
            validate_name("Миша123")

    def test_too_long_name(self):
        with pytest.raises(TooLongNameError):
            validate_name("О" * 20)

    def test_too_short_name(self):
        with pytest.raises(TooShortNameError):
            validate_name("М")

    def test_name_with_spaces(self):
        # isalpha will catch this too, but the validator checks letters first
        with pytest.raises(NameCanContainLettersError):
            validate_name("Ми ша")

    def test_name_lowercase_start(self):
        with pytest.raises(NameBeginCannotBeLowercaseError):
            validate_name("михаил")


class TestAgeValidator:

    def test_valid_date(self):
        d = validate_date_of_birth("2000-01-15")
        assert d.year == 2000
        assert d.month == 1
        assert d.day == 15

    def test_invalid_format(self):
        with pytest.raises(WrongAgeFormatError):
            validate_date_of_birth("01-15-2000")

    def test_garbage_input(self):
        with pytest.raises(WrongAgeFormatError):
            validate_date_of_birth("not-a-date")

