"""Use case: Search for an acquaintance candidate."""

import logging
from typing import Optional

from src.application.dto.acquaintance import AcquaintanceStatus, CandidateData, SearchResult
from src.domain.entities.user import Gender
from src.domain.exceptions import NonRegisteredError, ProfileMustBeActivatedError
from src.domain.interfaces.acquaintance_repository import IAcquaintanceRepository
from src.domain.interfaces.file_storage import IFileStorage

logger = logging.getLogger(__name__)


class SearchAcquaintanceUseCase:

    def __init__(
        self,
        acquaintance_repo: IAcquaintanceRepository,
        file_storage: IFileStorage,
    ) -> None:
        self._acquaintance_repo = acquaintance_repo
        self._file_storage = file_storage

    async def execute(self, sender_telegram_id: int) -> SearchResult:
        try:
            candidate = await self._acquaintance_repo.get_ranked_candidate(sender_telegram_id)
        except NonRegisteredError:
            return SearchResult(status=AcquaintanceStatus.NON_REGISTERED)
        except ProfileMustBeActivatedError:
            return SearchResult(status=AcquaintanceStatus.PROFILE_MUST_BE_ACTIVATED)
        except Exception as e:
            logger.exception('Unexpected error during search: %s', e)
            return SearchResult(status=AcquaintanceStatus.UNEXPECTED_ERROR)

        if candidate is None:
            return SearchResult(status=AcquaintanceStatus.NOT_FOUND)

        image = self._file_storage.get_file(str(candidate.telegram_id))

        candidate_data = CandidateData(
            user_id=candidate.telegram_id,
            name=candidate.name,
            age=str(candidate.date_of_birth),
            gender='Девушка' if candidate.gender == Gender.GIRL else 'Парень',
            description=candidate.description,
            image=image or b'',
        )

        return SearchResult(status=AcquaintanceStatus.FOUND, candidate=candidate_data)

