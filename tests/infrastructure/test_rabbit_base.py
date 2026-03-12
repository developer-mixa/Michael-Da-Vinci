"""Tests for infrastructure RabbitMQ base consumer."""

from types import SimpleNamespace

import msgpack
import pytest
from aio_pika.exceptions import QueueEmpty

from src.infrastructure.rabbit.base import BaseConsumer


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


class StubConsumer(BaseConsumer):
    __exchange_name__ = "test_exchange"

    def __init__(self, channel):
        self._rabbit_url = "amqp://fake"
        self._connection_pool = None
        self._channel_pool = None
        self._test_channel = channel

    async def channel(self):
        return self._test_channel

    async def processing_message(self, message):
        self.last_message = message


@pytest.mark.asyncio
async def test_declare_queue_binds_exchange():
    ch = DummyChannel()
    consumer = StubConsumer(ch)
    queue = await consumer.declare_queue("my_queue", routing_key="key")

    assert isinstance(queue, DummyQueue)
    assert ch.declared_queues[0][0] == "my_queue"
    assert queue.bound_exchange[1] == "key"


@pytest.mark.asyncio
async def test_base_produce_message():
    ch = DummyChannel()
    consumer = StubConsumer(ch)
    data = {"hello": "world"}
    await consumer.base_produce_message(data, queue="q1")

    assert len(ch.exchange.published) == 1
    msg_body, routing_key = ch.exchange.published[0]
    assert routing_key == "q1"
    assert msgpack.unpackb(msg_body.body) == data


@pytest.mark.asyncio
async def test_wait_answer_calls_callback(monkeypatch):
    ch = DummyChannel()
    consumer = StubConsumer(ch)

    async def fake_declare_queue(queue_name, exclusive=False, routing_key=None):
        q = DummyQueue()
        q.messages.append(SimpleNamespace(body=msgpack.packb(True)))
        return q

    monkeypatch.setattr(consumer, "declare_queue", fake_declare_queue)

    called = {}

    async def callback(value):
        called["value"] = value

    await consumer.wait_answer_for_user("reg_queue", 42, callback)
    assert called["value"] is True

