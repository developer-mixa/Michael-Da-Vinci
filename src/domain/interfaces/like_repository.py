"""Port: Like repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.like import Like


class ILikeRepository(ABC):

    @abstractmethod
    async def add_like(self, sender_user_id: UUID, target_user_id: UUID) -> Like:
        """Create a like (idempotent — return existing if already exists)."""

    @abstractmethod
    async def get_likes_count(self, user_id: UUID) -> int:
        """Return number of likes received by user."""

