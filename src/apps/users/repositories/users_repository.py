from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.users.model.models import User

class UsersRepository:
    
    def __init__(self, async_session: AsyncSession) -> None:
        self.__session = async_session
    
    async def get_users(self):
        result = await self.__session.execute(select(User))
        return result.scalars().all()
