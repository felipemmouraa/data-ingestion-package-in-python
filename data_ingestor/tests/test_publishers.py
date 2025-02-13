# tests/test_publisher.py
import json
import pytest
from app.publishers.publisher import Publisher

@pytest.fixture
def publisher():
    p = Publisher()
    yield p
    p.close()

def test_publish_message(publisher, monkeypatch):
    published = []

    # Monkey-patch the channel's basic_publish to capture messages
    def fake_publish(exchange, routing_key, body, properties):
        published.append((routing_key, json.loads(body)))

    publisher.channel.basic_publish = fake_publish
    sample_message = {"test": "data"}
    publisher.publish("test_queue", sample_message)
    assert published[0][0] == "test_queue"
    assert published[0][1] == sample_message
