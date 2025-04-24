from datetime import date
from random import choice
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, select

from src.apps.consumers.common.data.user_repository import UserRepository
from src.apps.consumers.errors.errors import ProfileMustBeActivatedError
from src.apps.consumers.model.models import Like, User, UserStatus
from src.storage.db import async_session
from src.storage.redis import get_redis, setup_redis

import json
import logging

logger = logging.getLogger(__name__)

class AcquaintanceRepository(UserRepository):
    def __init__(self):
        super().__init__()
        setup_redis()

    async def get_user_likes_count(self, user_id: UUID) -> int:
        async with async_session() as db:
            result = await db.scalar(
                select(func.count())
                .where(Like.target_user_id == user_id)
            )
            return result or 0

    async def get_ranked_acquaintance(self, sender_user_tg_id: int) -> User | None:
        user: User = await self.get_user_by_telegram_id(sender_user_tg_id)
        if user.status == UserStatus.NO_ACTIVE:
            raise ProfileMustBeActivatedError()

        user_age = self.__calculate_age(user.date_of_birth)
        redis = get_redis()

        cache_key = f"acquaintance_candidates:{sender_user_tg_id}"
        index_key = f"acquaintance_index:{sender_user_tg_id}"

        cached_users = await redis.get(cache_key)
        if not cached_users:
            async with async_session() as db:
                result = await db.execute(
                    select(User).where(
                        User.telegram_id != sender_user_tg_id,
                        User.status == UserStatus.ACTIVE,
                        User.gender != user.gender,
                    )
                )
                candidates = result.scalars().all()

            if not candidates:
                return None

            candidates_with_metrics = []
            for candidate in candidates:
                age_diff = abs(self.__calculate_age(candidate.date_of_birth) - user_age)
                likes = await self.get_user_likes_count(candidate.id)
                
                # Чем меньше возрастная разница и больше лайков - тем лучше
                score = (age_diff * 0.6) - (likes * 0.4)
                
                candidates_with_metrics.append({
                    'user': candidate,
                    'age_diff': age_diff,
                    'likes': likes,
                    'score': score
                })

            candidates_with_metrics.sort(key=lambda x: x['score'])
            
            sorted_candidates = [item['user'] for item in candidates_with_metrics]

            logger.info("Ранжирование кандидатов:")
            for item in candidates_with_metrics:
                logger.info(
                    f"ID: {item['user'].id} | "
                    f"Возраст: {self.__calculate_age(item['user'].date_of_birth)} | "
                    f"Δ возраста: {item['age_diff']} | "
                    f"Лайки: {item['likes']} | "
                    f"Общий счёт: {item['score']:.2f}"
                )

            await redis.set(
                cache_key,
                json.dumps([u.to_dict() for u in sorted_candidates]),
                ex=3600
            )
            await redis.set(index_key, 0)
        else:
            sorted_candidates = [User.from_dict(u) for u in json.loads(cached_users)]

        current_index = int(await redis.get(index_key) or 0)
        
        if current_index >= len(sorted_candidates):
            current_index = 0
            await redis.set(index_key, current_index)

        selected = sorted_candidates[current_index]
        
        logger.info(
            f"Selected candidate ID: {selected.id} "
            f"(Index: {current_index}/{len(sorted_candidates)})"
        )

        await redis.set(index_key, current_index + 1)
        return selected

    def __calculate_age(self, birth_date: date) -> int:
        today = date.today()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
