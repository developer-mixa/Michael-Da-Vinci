"""Consumer application wrapper (FastAPI + consumer in lifespan)."""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from src.infrastructure.rabbit.consumer_runner import ConsumerRunner
from src.presentation.api.analytics.router import router as analytics_router

logger = logging.getLogger(__name__)

RUNNER: ConsumerRunner


class ConsumerApp:

    URL_TEMPLATE = 'src.presentation.consumers.consumer_app:create_app'

    def __init__(self, runner: ConsumerRunner, port: int) -> None:
        global RUNNER
        RUNNER = runner
        self._port = port

    def build(self) -> None:
        uvicorn.run(self.URL_TEMPLATE, factory=True, host='0.0.0.0', port=self._port, workers=1)

    @asynccontextmanager
    @staticmethod
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info('Starting lifespan')
        task = asyncio.create_task(RUNNER._run())
        logger.info('Started successfully')
        yield
        task.cancel()
        logger.info('Ending lifespan')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=ConsumerApp.lifespan)
    app.include_router(analytics_router, prefix='', tags=['tech'])
    return app

