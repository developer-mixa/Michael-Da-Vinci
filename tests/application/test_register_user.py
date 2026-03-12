"""Tests for RegisterUserUseCase."""

import base64
from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.dto.registration import RegistrationInput
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.exceptions import AlreadyRegisteredError


@pytest.fixture
def user_repo():
    repo = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def file_storage():
    return MagicMock()


@pytest.fixture
def use_case(user_repo, file_storage):
    return RegisterUserUseCase(user_repo, file_storage)


async def test_register_user_success(use_case, user_repo, file_storage):
    image_bytes = b"fake_image_data"
    image_b64 = base64.b64encode(image_bytes).decode()

    data = RegistrationInput(
        user_id=123,
        name="Михаил",
        age="2000-01-15",
        gender="Парень",
        description="Привет",
        image_base64=image_b64,
    )

    result = await use_case.execute(data)

    assert result is True
    user_repo.create.assert_awaited_once()
    file_storage.upload_file.assert_called_once()


async def test_register_user_already_exists(use_case, user_repo, file_storage):
    user_repo.create.side_effect = AlreadyRegisteredError()
    image_b64 = base64.b64encode(b"img").decode()

    data = RegistrationInput(
        user_id=123,
        name="Михаил",
        age="2000-01-15",
        gender="Парень",
        description="Привет",
        image_base64=image_b64,
    )

    result = await use_case.execute(data)

    assert result is False
    file_storage.upload_file.assert_not_called()

