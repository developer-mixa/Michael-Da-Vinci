from redis.asyncio import ConnectionPool, Redis

from config.settings import settings

redis: Redis


def setup_redis() -> None:
    global redis

    pool = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3, password=settings.REDIS_PASSWORD, socket_timeout=5)
    redis = Redis(connection_pool=pool)


def get_redis() -> Redis:
    global redis

    return redis