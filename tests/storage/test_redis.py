from src.storage import redis as redis_storage


def test_setup_redis_uses_settings(monkeypatch):
    created = {}

    class DummyPool:
        def __init__(self, **kwargs):
            created["pool_kwargs"] = kwargs

    class DummyRedis:
        def __init__(self, connection_pool):
            created["redis_pool"] = connection_pool

    monkeypatch.setattr(redis_storage, "ConnectionPool", lambda **kwargs: DummyPool(**kwargs))
    monkeypatch.setattr(redis_storage, "Redis", lambda connection_pool: DummyRedis(connection_pool))

    redis_storage.setup_redis()

    pool_kwargs = created["pool_kwargs"]
    assert pool_kwargs["db"] == 3
    assert pool_kwargs["socket_timeout"] == 5
    assert "host" in pool_kwargs
    assert "port" in pool_kwargs

    r = redis_storage.get_redis()
    assert isinstance(r, DummyRedis)


