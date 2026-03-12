"""Infrastructure: Acquaintance ranking repository (Postgres + Redis cache)."""

import json
import logging
from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities.user import Gender, User, UserStatus
from src.domain.exceptions import NonRegisteredError, ProfileMustBeActivatedError
from src.domain.interfaces.acquaintance_repository import IAcquaintanceRepository
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.like_repository import ILikeRepository
from src.infrastructure.database.mappers import user_model_to_domain
from src.infrastructure.database.models import UserModel, UserStatusDB

logger = logging.getLogger(__name__)


class SqlAlchemyAcquaintanceRepository(IAcquaintanceRepository):

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        cache: ICache,
        like_repo: ILikeRepository,
    ) -> None:
        self._session_factory = session_factory
        self._cache = cache
        self._like_repo = like_repo

    async def get_ranked_candidate(self, sender_telegram_id: int) -> Optional[User]:
        # Get sender from DB
        async with self._session_factory() as db:
            sender_model = await db.scalar(
                select(UserModel).where(UserModel.telegram_id == sender_telegram_id)
            )
            if not sender_model:
                raise NonRegisteredError()
            sender = user_model_to_domain(sender_model)

        if not sender.is_active:
            raise ProfileMustBeActivatedError()

        sender_age = sender.age

        cache_key = f'acquaintance_candidates:{sender_telegram_id}'
        index_key = f'acquaintance_index:{sender_telegram_id}'

        cached = await self._cache.get(cache_key)
        if not cached:
            # Fetch candidates from DB
            async with self._session_factory() as db:
                result = await db.execute(
                    select(UserModel).where(
                        UserModel.telegram_id != sender_telegram_id,
                        UserModel.status == UserStatusDB.ACTIVE,
                        UserModel.gender != sender_model.gender,
                    )
                )
                candidate_models = result.scalars().all()

            if not candidate_models:
                return None

            candidates_with_metrics = []
            for cm in candidate_models:
                candidate = user_model_to_domain(cm)
                age_diff = abs(candidate.age - sender_age)
                likes = await self._like_repo.get_likes_count(candidate.id)
                score = (age_diff * 0.6) - (likes * 0.4)
                candidates_with_metrics.append({
                    'user': candidate,
                    'model_dict': cm.to_dict(),
                    'score': score,
                })

            candidates_with_metrics.sort(key=lambda x: x['score'])
            sorted_dicts = [item['model_dict'] for item in candidates_with_metrics]

            await self._cache.set(cache_key, json.dumps(sorted_dicts), ttl=3600)
            await self._cache.set(index_key, '0')

            sorted_users = [item['user'] for item in candidates_with_metrics]
        else:
            sorted_dicts = json.loads(cached)
            sorted_users = []
            for d in sorted_dicts:
                sorted_users.append(User(
                    id=d['id'],
                    name=d['name'],
                    description=d['description'],
                    date_of_birth=date.fromisoformat(d['date_of_birth']),
                    telegram_id=d['telegram_id'],
                    status=UserStatus(d['status']),
                    gender=Gender(d['gender']),
                ))

        current_index = int(await self._cache.get(index_key) or '0')

        if current_index >= len(sorted_users):
            current_index = 0
            await self._cache.set(index_key, str(current_index))

        selected = sorted_users[current_index]
        await self._cache.set(index_key, str(current_index + 1))

        return selected

