import types

from src.storage import rabbit


async def test_get_connection_uses_settings(monkeypatch):
    called = {}

    async def fake_connect_robust(url):
        called["url"] = url
        return types.SimpleNamespace(url=url)

    monkeypatch.setattr(rabbit.aio_pika, "connect_robust", fake_connect_robust)

    conn = await rabbit.get_connection()
    assert conn.url == called["url"]
    assert called["url"].startswith("amqp://")


