import asyncio
from types import SimpleNamespace

import msgpack
import pytest
from aio_pika.exceptions import QueueEmpty

from src.apps.consumers.base.base_consumer import BaseConsumer


class DummyConsumer(BaseConsumer):
    __exchange_name__ = "test_exchange"

    def __init__(self, channel):
        self._channel = channel

    async def channel(self):
        return self._channel

    async def processing_message(self, message):
        # used only in other tests
        self.last_message = message


class DummyQueue:
    def __init__(self):
        self.bound_exchange = None
        self.messages = []

    async def bind(self, exchange, routing_key=None):
        self.bound_exchange = (exchange, routing_key)

    async def get(self, no_ack=True):
        if not self.messages:
            raise QueueEmpty
        return self.messages.pop(0)

    async def iterator(self):
        for m in list(self.messages):
            yield m


class DummyExchange:
    def __init__(self):
        self.published = []

    async def publish(self, message, routing_key):
        self.published.append((message, routing_key))


class DummyChannel:
    def __init__(self):
        self.declared_queues = []
        self.exchange = DummyExchange()
        self.qos = None

    async def declare_exchange(self, name, durable=True):
        self.exchange_name = (name, durable)

    async def declare_queue(self, name, exclusive=False):
        q = DummyQueue()
        self.declared_queues.append((name, exclusive, q))
        return q

    async def get_exchange(self, name):
        return self.exchange

    async def set_qos(self, prefetch_count=1):
        self.qos = prefetch_count


@pytest.mark.asyncio
async def test_declare_queue_binds_exchange():
    channel = DummyChannel()
    consumer = DummyConsumer(channel)

    queue = await consumer.declare_queue("test_queue", routing_key="key", exclusive=False)

    # queue created and bound
    assert isinstance(queue, DummyQueue)
    assert channel.declared_queues[0][0] == "test_queue"
    assert queue.bound_exchange[1] == "key"


@pytest.mark.asyncio
async def test_base_produce_message_publishes_msgpack():
    channel = DummyChannel()
    consumer = DummyConsumer(channel)

    data = {"foo": "bar"}
    await consumer.base_produce_message(data, queue="test_queue")

    assert len(channel.exchange.published) == 1
    message, routing_key = channel.exchange.published[0]
    assert routing_key == "test_queue"
    unpacked = msgpack.unpackb(message.body)
    assert unpacked == data


@pytest.mark.asyncio
async def test_wait_answer_for_user_calls_callback_on_message(monkeypatch):
    channel = DummyChannel()
    consumer = DummyConsumer(channel)

    # Prepare queue with single boolean message
    async def fake_declare_queue(queue_name, exclusive=False, routing_key=None):
        q = DummyQueue()
        q.messages.append(SimpleNamespace(body=msgpack.packb(True)))
        return q

    monkeypatch.setattr(consumer, "declare_queue", fake_declare_queue)

    called = {}

    async def success_callback(value: bool):
        called["value"] = value

    await consumer.wait_answer_for_user(
        queue_name="user_registration",
        user_id=123,
        success_callback=success_callback,
    )

    assert called.get("value") is True


