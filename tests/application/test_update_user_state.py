"""Tests for UpdateUserStateUseCase."""

from datetime import date
from unittest.mock import AsyncMock

import pytest

from src.application.dto.update_user import UpdateUserInput
from src.application.use_cases.update_user_state import UpdateUserStateUseCase
from src.domain.entities.user import Gender, User, UserStatus
from src.domain.exceptions import NonRegisteredError


@pytest.fixture
def user_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def use_case(user_repo):
    return UpdateUserStateUseCase(user_repo)


async def test_update_name(use_case, user_repo):
    user = User(
        name="Старое",
        description="Описание",
        date_of_birth=date(2000, 1, 1),
        telegram_id=123,
        status=UserStatus.ACTIVE,
        gender=Gender.MAN,
    )
    user_repo.get_by_telegram_id.return_value = user

    data = UpdateUserInput(user_id=123, name="Новое")
    result = await use_case.execute(data)

    assert result is True
    assert user.name == "Новое"
    user_repo.update.assert_awaited_once_with(user)


async def test_activate_profile(use_case, user_repo):
    user = User(
        name="Тест",
        description="Описание",
        date_of_birth=date(2000, 1, 1),
        telegram_id=123,
        status=UserStatus.NO_ACTIVE,
        gender=Gender.MAN,
    )
    user_repo.get_by_telegram_id.return_value = user

    data = UpdateUserInput(user_id=123, status=True)
    result = await use_case.execute(data)

    assert result is True
    assert user.status == UserStatus.ACTIVE


async def test_update_not_registered(use_case, user_repo):
    user_repo.get_by_telegram_id.side_effect = NonRegisteredError()

    data = UpdateUserInput(user_id=999, name="Тест")
    result = await use_case.execute(data)

    assert result is False

