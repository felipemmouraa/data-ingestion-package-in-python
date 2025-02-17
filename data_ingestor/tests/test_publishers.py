import json
import pika
import pytest
from app.publishers.publisher import Publisher

class DummyChannel:
    def __init__(self):
        self.messages = []

    def queue_declare(self, queue, durable):
        self.declared = True

    def basic_publish(self, exchange, routing_key, body, properties):
        self.messages.append((exchange, routing_key, body, properties))

class DummyConnection:
    def __init__(self):
        self._channel = DummyChannel()

    def channel(self):
        return self._channel

    def close(self):
        pass

def dummy_blocking_connection(params):
    return DummyConnection()

def test_publisher(monkeypatch):
    monkeypatch.setattr(pika, "BlockingConnection", dummy_blocking_connection)

    publisher = Publisher()

    sample_queue = "test_queue"
    sample_message = {"test": "data"}

    publisher.publish(sample_queue, sample_message)

    dummy_channel = publisher.channel
    assert len(dummy_channel.messages) == 1

    exchange, routing_key, body, properties = dummy_channel.messages[0]

    assert exchange == ""

    assert routing_key == sample_queue

    assert json.loads(body) == sample_message