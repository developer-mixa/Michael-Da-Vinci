from datetime import date
from random import choice
from typing import List

from sqlalchemy import select

from src.apps.consumers.common.data.user_repository import UserRepository
from src.apps.consumers.errors.errors import ProfileMustBeActivatedError
from src.apps.consumers.model.models import User, UserStatus
from src.storage.db import async_session
from src.storage.redis import get_redis, setup_redis

import json
import logging

logger = logging.getLogger(__name__)


class AcquaintanceRepository(UserRepository):
    def __init__(self):
        super().__init__()
        setup_redis()

    async def get_random_acquaintance(self, sender_user_tg_id: int) -> User | None:
        user: User = await self.get_user_by_telegram_id(sender_user_tg_id)

        if user.status == UserStatus.NO_ACTIVE:
            raise ProfileMustBeActivatedError()

        async with async_session() as db:
            users_scalars = await db.scalars(
                select(User).where(
                    User.telegram_id != sender_user_tg_id,
                    User.status == UserStatus.ACTIVE,
                    User.gender != user.gender,
                )
            )

            users = users_scalars.all()

            return choice(users) if len(users) > 0 else None
        
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

            candidates.sort(key=lambda u: abs(self.__calculate_age(u.date_of_birth) - user_age))

            await redis.set(
                cache_key,
                json.dumps([u.to_dict() for u in candidates]),
                ex=3600
            )
            await redis.set(index_key, 0)
        else:
            candidates = [User.from_dict(u) for u in json.loads(cached_users)]

        current_index = int(await redis.get(index_key) or 0)
        
        if current_index >= len(candidates):
            current_index = 0
            await redis.set(index_key, current_index)

        # for c in candidates:
        #     logger.info("d: %s", c.date_of_birth)
        #     logger.info('index %s', current_index)

        selected = candidates[current_index]

        await redis.set(index_key, current_index + 1)

        return selected


    def __calculate_age(self, birth_date: date) -> int:
        today = date.today()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
