import types

from src.storage import db


def test_create_engine_uses_settings_db_url(monkeypatch):
    called = {}

    def fake_create_async_engine(url, **kwargs):
        called["url"] = url
        called["kwargs"] = kwargs
        # return a simple dummy object
        return types.SimpleNamespace(url=url, kwargs=kwargs)

    monkeypatch.setattr(db, "create_async_engine", fake_create_async_engine)

    engine = db.create_engine()

    assert "postgresql" in called["url"]
    assert engine.url == called["url"]
    assert "poolclass" in called["kwargs"]
    assert "connect_args" in called["kwargs"]


async def test_get_db_yields_session(monkeypatch):
    class DummySessionCtx:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummyAsyncSessionMaker:
        def __call__(self):
            # mimic async_session() returning an async context manager
            return DummySessionCtx()

    monkeypatch.setattr(db, "async_session", DummyAsyncSessionMaker())

    gen = db.get_db()
    session = await gen.__anext__()
    assert isinstance(session, DummySessionCtx)


