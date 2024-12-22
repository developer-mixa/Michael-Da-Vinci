from sqlalchemy import select

from src.apps.consumers.errors.errors import NonRegisteredError
from src.apps.consumers.model.models import User
from src.storage.db import async_session


class UserRepository:

    async def get_user_by_telegram_id(self, user_tg_id: int) -> User:
        async with async_session() as db:
            user = await db.scalar(select(User).where(User.telegram_id == user_tg_id))
            if not user:
                raise NonRegisteredError
            return user
