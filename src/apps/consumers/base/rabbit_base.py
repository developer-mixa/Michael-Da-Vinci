from typing import Any

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.channel import Channel
from aio_pika.connection import Connection
from aio_pika.pool import Pool

from config.settings import settings
from src.apps.consumers.base.exceptions import RabbitException


class RabbitBase:
    def __init__(self) -> None:
        self._connection_pool: Pool[Connection] | None = None
        self._channel_pool: Pool[Channel] | None = None

    async def __get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(settings.rabbit_url)

    async def __get_channel(self) -> AbstractChannel:
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()

    async def channel(self) -> Channel:
        if self._channel_pool is None:
            raise RabbitException('Please use context manager for Rabbit helper.')
        async with self._channel_pool.acquire() as channel:
            return channel

    async def connection(self) -> Connection:
        if not self._connection_pool:
            raise RabbitException('Please use context manager for Rabbit helper.')
        async with self._connection_pool.acquire() as connection:
            return connection

    async def __aenter__(self):
        self._connection_pool = Pool(self.__get_connection, max_size=2)
        self._channel_pool = Pool(self.__get_channel, max_size=10)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self._channel_pool.is_closed:
            await self._channel_pool.close()
        if not self._connection_pool.is_closed:
            await self._connection_pool.close()
