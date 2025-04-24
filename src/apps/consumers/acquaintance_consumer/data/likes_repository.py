from uuid import UUID
from datetime import datetime

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.consumers.model.models import Like
from src.storage.db import async_session

import logging

logger = logging.getLogger(__name__)

class LikeRepository:
    async def like_user(
        self, 
        sender_user_id: UUID,
        target_user_id: UUID
    ) -> Like:
        async with async_session() as db:
            existing_like = await self._find_like(sender_user_id, target_user_id, db)
            
            if existing_like:
                return existing_like

            new_like = Like(
                sender_user_id=sender_user_id,
                target_user_id=target_user_id
            )
            
            db.add(new_like)
            await db.commit()
            
            logger.info(f'Like between {str(sender_user_id)} and {str(target_user_id)} was added to db!')

            return new_like

    async def unlike_user(
        self,
        sender_user_id: UUID,
        target_user_id: UUID
    ) -> bool:
        async with async_session() as db:
            like = await self._find_like(sender_user_id, target_user_id, db)
            
            if like:
                await db.delete(like)
                await db.commit()
                return True
            
            return False


    async def _find_like(
        self, 
        sender_user_id: UUID,
        target_user_id: UUID,
        db: AsyncSession
    ) -> Like | None:
        result = await db.execute(
            select(Like)
            .where(
                and_(
                    Like.sender_user_id == sender_user_id,
                    Like.target_user_id == target_user_id
                )
            )
        )
        return result.scalar()