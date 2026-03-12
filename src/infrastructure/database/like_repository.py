"""Infrastructure: SQLAlchemy implementation of ILikeRepository."""

import logging
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities.like import Like as DomainLike
from src.domain.interfaces.like_repository import ILikeRepository
from src.infrastructure.database.mappers import like_model_to_domain
from src.infrastructure.database.models import LikeModel

logger = logging.getLogger(__name__)


class SqlAlchemyLikeRepository(ILikeRepository):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def add_like(self, sender_user_id: UUID, target_user_id: UUID) -> DomainLike:
        async with self._session_factory() as db:
            existing = await db.scalar(
                select(LikeModel).where(
                    and_(
                        LikeModel.sender_user_id == sender_user_id,
                        LikeModel.target_user_id == target_user_id,
                    )
                )
            )
            if existing:
                return like_model_to_domain(existing)

            new_like = LikeModel(
                sender_user_id=sender_user_id,
                target_user_id=target_user_id,
            )
            db.add(new_like)
            await db.commit()
            logger.info('Like between %s and %s added', sender_user_id, target_user_id)
            return like_model_to_domain(new_like)

    async def get_likes_count(self, user_id: UUID) -> int:
        async with self._session_factory() as db:
            result = await db.scalar(
                select(func.count()).where(LikeModel.target_user_id == user_id)
            )
            return result or 0

