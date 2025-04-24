from redis.asyncio import ConnectionPool, Redis

from config.settings import settings

redis_: Redis


def setup_redis() -> None:
    global redis_

    pool = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3, password=settings.REDIS_PASSWORD, socket_timeout=5)
    redis_ = Redis(connection_pool=pool)


def get_redis() -> Redis:
    global redis_

    return redis_