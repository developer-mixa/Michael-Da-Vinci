"""Port: User repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User:
        """Return user or raise NonRegisteredError."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Persist a new user. Raise AlreadyRegisteredError on duplicate."""

    @abstractmethod
    async def update(self, user: User) -> None:
        """Save changes to an existing user."""

