"""Tests for SearchAcquaintanceUseCase."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.dto.acquaintance import AcquaintanceStatus
from src.application.use_cases.search_acquaintance import SearchAcquaintanceUseCase
from src.domain.entities.user import Gender, User, UserStatus
from src.domain.exceptions import NonRegisteredError, ProfileMustBeActivatedError


@pytest.fixture
def acquaintance_repo():
    return AsyncMock()


@pytest.fixture
def file_storage():
    return MagicMock()


@pytest.fixture
def use_case(acquaintance_repo, file_storage):
    return SearchAcquaintanceUseCase(acquaintance_repo, file_storage)


async def test_search_found(use_case, acquaintance_repo, file_storage):
    candidate = User(
        name="Анна",
        description="Привет",
        date_of_birth=date(2001, 5, 20),
        telegram_id=456,
        status=UserStatus.ACTIVE,
        gender=Gender.GIRL,
    )
    acquaintance_repo.get_ranked_candidate.return_value = candidate
    file_storage.get_file.return_value = b"photo_data"

    result = await use_case.execute(123)

    assert result.status == AcquaintanceStatus.FOUND
    assert result.candidate is not None
    assert result.candidate.name == "Анна"
    assert result.candidate.image == b"photo_data"


async def test_search_not_found(use_case, acquaintance_repo):
    acquaintance_repo.get_ranked_candidate.return_value = None

    result = await use_case.execute(123)
    assert result.status == AcquaintanceStatus.NOT_FOUND


async def test_search_non_registered(use_case, acquaintance_repo):
    acquaintance_repo.get_ranked_candidate.side_effect = NonRegisteredError()

    result = await use_case.execute(123)
    assert result.status == AcquaintanceStatus.NON_REGISTERED


async def test_search_profile_not_activated(use_case, acquaintance_repo):
    acquaintance_repo.get_ranked_candidate.side_effect = ProfileMustBeActivatedError()

    result = await use_case.execute(123)
    assert result.status == AcquaintanceStatus.PROFILE_MUST_BE_ACTIVATED

