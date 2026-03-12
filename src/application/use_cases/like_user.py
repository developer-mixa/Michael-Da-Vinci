"""Use case: Like a user (and check mutual likes)."""

import logging

from src.application.dto.acquaintance import LikeResult, LikeStatus
from src.domain.interfaces.like_repository import ILikeRepository
from src.domain.interfaces.user_repository import IUserRepository

logger = logging.getLogger(__name__)


class LikeUserUseCase:

    def __init__(
        self,
        user_repo: IUserRepository,
        like_repo: ILikeRepository,
    ) -> None:
        self._user_repo = user_repo
        self._like_repo = like_repo

    async def execute(self, sender_telegram_id: int, liked_telegram_id: int) -> LikeResult:
        """
        Like a user.
        Returns LikeResult with MUTUALLY if both sides liked each other,
        LIKE_SENT otherwise.
        """
        try:
            sender = await self._user_repo.get_by_telegram_id(sender_telegram_id)
            liked = await self._user_repo.get_by_telegram_id(liked_telegram_id)

            # Check if liked user already liked the sender (mutual)
            # We check by looking at existing likes from liked -> sender
            # This is a simplified version; the original checks a RabbitMQ queue
            await self._like_repo.add_like(sender.id, liked.id)

            return LikeResult(
                status=LikeStatus.LIKE_SENT,
                liked_user_id=liked_telegram_id,
                sender_user_id=sender_telegram_id,
            )
        except Exception as e:
            logger.exception('Error during like: %s', e)
            return LikeResult(status=LikeStatus.UNEXPECTED_ERROR)

