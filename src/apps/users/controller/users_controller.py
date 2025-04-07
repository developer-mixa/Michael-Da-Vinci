from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.apps.users.router import router
from src.storage.db import get_db
from sqlalchemy import select
from src.apps.consumer.model.models import User

import logging

logger = logging.getLogger(__name__)

@router.get('/')
async def get_users(session: AsyncSession = Depends(get_db),) -> JSONResponse:
    print(session.execute(select(User)))
    logger.info("asdasdasdasdasdasd")
    return {"12": "12"}