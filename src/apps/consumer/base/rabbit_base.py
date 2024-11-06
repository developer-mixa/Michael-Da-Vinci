from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from aio_pika.channel import Channel
from aio_pika.connection import  Connection

from src.apps.consumer.base.exceptions import RabbitException
import aio_pika
from config.settings import settings
from aio_pika.pool import Pool


class RabbitBase:
    def __init__(self):
        self._connection_pool: Pool[Connection] | None = None
        self._channel_pool: Pool[Channel] | None = None

    async def __get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(settings.rabbit_url)

    async def __get_channel(self) -> AbstractChannel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()


    async def channel(self) -> Channel:
        if self._channel_pool is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        async with self._channel_pool.acquire() as channel:
            return channel


    async def connection(self) -> Connection:
        if not self._connection_pool:
            raise RabbitException("Please use context manager for Rabbit helper.")
        async with self._connection_pool.acquire() as connection:
            return connection

    def __enter__(self):
        self._connection_pool = Pool(self.__get_connection, max_size=2)
        self._channel_pool = Pool(self.__get_channel, max_size=10)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._channel_pool.is_closed:
            self._channel_pool.close()
        if not self._connection_pool.is_closed:
            self._connection_pool.close()