from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
import uvicorn
from src.apps.consumers.base.runner import ConsumerRunner

from src.apps.api.analytics.router import router as analytics_router

import logging
import asyncio

logger = logging.getLogger(__name__)

RUNNER: ConsumerRunner

class ConsumerApp:

    URL_TEMPLATE = 'src.apps.consumers.base.consumer_app:create_app'

    def __init__(self, runner: ConsumerRunner, port: int):
        global RUNNER
        RUNNER = runner
        self.__port = port
    
    def build(self):
        uvicorn.run(self.URL_TEMPLATE, factory=True, host='0.0.0.0', port=self.__port, workers=1)

    @asynccontextmanager
    @staticmethod
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info('Starting lifespan')
        task = asyncio.create_task(RUNNER._run())
        logger.info('Started succesfully')
        yield
        task.cancel()
        logger.info('Ending lifespan')

def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=ConsumerApp.lifespan)
    app.include_router(analytics_router, prefix='', tags=['tech'])
    return app