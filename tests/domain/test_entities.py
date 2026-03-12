"""Tests for domain entities."""

from datetime import date
from uuid import uuid4

from src.domain.entities.user import Gender, User, UserStatus
from src.domain.entities.like import Like


def test_user_age_calculation():
    user = User(
        name="Тест",
        description="Тест",
        date_of_birth=date(2000, 1, 1),
        telegram_id=123,
        status=UserStatus.ACTIVE,
        gender=Gender.MAN,
    )
    assert user.age > 0
    assert user.age == date.today().year - 2000 - (
        (date.today().month, date.today().day) < (1, 1)
    )


def test_user_is_active():
    user = User(
        name="Тест",
        description="Тест",
        date_of_birth=date(2000, 1, 1),
        telegram_id=123,
        status=UserStatus.ACTIVE,
        gender=Gender.MAN,
    )
    assert user.is_active is True


def test_user_is_not_active():
    user = User(
        name="Тест",
        description="Тест",
        date_of_birth=date(2000, 1, 1),
        telegram_id=123,
        status=UserStatus.NO_ACTIVE,
        gender=Gender.MAN,
    )
    assert user.is_active is False


def test_like_creation():
    sender = uuid4()
    target = uuid4()
    like = Like(sender_user_id=sender, target_user_id=target)
    assert like.sender_user_id == sender
    assert like.target_user_id == target
    assert like.id is None

