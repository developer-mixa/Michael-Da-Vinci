"""Use case: Update user profile fields or status."""

import logging

from src.application.dto.update_user import UpdateUserInput
from src.domain.entities.user import UserStatus
from src.domain.exceptions import NonRegisteredError
from src.domain.interfaces.user_repository import IUserRepository

logger = logging.getLogger(__name__)


class UpdateUserStateUseCase:

    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, data: UpdateUserInput) -> bool:
        """
        Update user fields.
        Returns True on success, False if user not found.
        """
        try:
            user = await self._user_repo.get_by_telegram_id(data.user_id)
        except NonRegisteredError:
            logger.info('User %s not found for update', data.user_id)
            return False

        if data.name is not None:
            user.name = data.name
        if data.description is not None:
            user.description = data.description
        if data.status is not None:
            user.status = UserStatus.ACTIVE if data.status else UserStatus.NO_ACTIVE

        await self._user_repo.update(user)
        logger.info('User %s updated successfully', data.user_id)
        return True

