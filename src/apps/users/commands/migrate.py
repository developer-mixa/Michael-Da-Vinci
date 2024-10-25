import asyncio
import logging

from sqlalchemy.exc import IntegrityError

from src.apps.common.models import meta
from src.storage.db import engine


async def migrate():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(meta.metadata.create_all)
            await conn.commit()
            print(meta.metadata.tables)
    except IntegrityError:
        logging.exception('Already exists')


if __name__ == '__main__':
    asyncio.run(migrate())