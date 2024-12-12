from sqlalchemy import select
from random import choice
from src.apps.consumers.model.models import User, UserStatus
from src.apps.consumers.errors.errors import NonRegisteredError
from src.storage.db import async_session

class AcquaintanceRepository:
    async def get_random_acquaintance(self, user_tg_id) -> User | None:
        async with async_session() as db:
            user: User = await db.scalar(select(User).where(User.telegram_id == user_tg_id))

            if not user:
                raise NonRegisteredError

            users_scalars = await db.scalars(select(User).where(
                User.telegram_id != user_tg_id,
                User.status == UserStatus.ACTIVE,
                User.gender != user.gender
                )
            )

            users = users_scalars.all()
            
            return choice(users) if len(users) > 0 else None
    