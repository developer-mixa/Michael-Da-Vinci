"""Infrastructure: Redis implementation of ICache."""

from typing import Optional

from redis.asyncio import ConnectionPool, Redis

from src.domain.interfaces.cache import ICache


class RedisCache(ICache):

    def __init__(self, host: str, port: int, password: str, db: int = 3) -> None:
        pool = ConnectionPool(host=host, port=port, db=db, password=password, socket_timeout=5)
        self._redis = Redis(connection_pool=pool)

    @property
    def redis(self) -> Redis:
        """Expose underlying Redis instance (needed by aiogram RedisStorage)."""
        return self._redis

    async def get(self, key: str) -> Optional[str]:
        value = await self._redis.get(key)
        if value is not None:
            return value.decode() if isinstance(value, bytes) else value
        return None

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        if ttl:
            await self._redis.set(key, value, ex=ttl)
        else:
            await self._redis.set(key, value)

