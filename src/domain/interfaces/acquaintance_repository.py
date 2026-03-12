"""Port: Acquaintance (matching) repository interface."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class IAcquaintanceRepository(ABC):

    @abstractmethod
    async def get_ranked_candidate(self, sender_telegram_id: int) -> Optional[User]:
        """
        Return the next best candidate for the given user,
        or None if nobody is available.
        Raises NonRegisteredError / ProfileMustBeActivatedError as needed.
        """

