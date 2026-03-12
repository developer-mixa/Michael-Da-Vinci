"""Infrastructure: SQLAlchemy implementation of IUserRepository."""

import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.entities.user import User, UserStatus
from src.domain.exceptions import AlreadyRegisteredError, NonRegisteredError
from src.domain.interfaces.user_repository import IUserRepository
from src.infrastructure.database.mappers import user_domain_to_model, user_model_to_domain
from src.infrastructure.database.models import UserModel, UserStatusDB

logger = logging.getLogger(__name__)


class SqlAlchemyUserRepository(IUserRepository):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        async with self._session_factory() as db:
            model = await db.scalar(
                select(UserModel).where(UserModel.telegram_id == telegram_id)
            )
            if not model:
                raise NonRegisteredError()
            return user_model_to_domain(model)

    async def create(self, user: User) -> User:
        async with self._session_factory() as db:
            model = user_domain_to_model(user)
            db.add(model)
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise AlreadyRegisteredError()
            return user_model_to_domain(model)

    async def update(self, user: User) -> None:
        async with self._session_factory() as db:
            model = await db.scalar(
                select(UserModel).where(UserModel.telegram_id == user.telegram_id)
            )
            if not model:
                raise NonRegisteredError()

            model.name = user.name
            model.description = user.description
            model.date_of_birth = user.date_of_birth
            model.status = UserStatusDB(user.status.value)

            await db.commit()

