from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.apps.users.router import router
from src.storage.db import get_db

@router.get('/')
async def get_users(session: AsyncSession = Depends(get_db),) -> JSONResponse:
    pass