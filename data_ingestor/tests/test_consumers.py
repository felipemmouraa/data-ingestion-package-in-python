import json
import pytest
from app.consumers.consumer import process_message, callback

class DummyRawDataService:
    def __init__(self):
        self.called = False
        self.data = None

    def save_raw_data(self, data: dict):
        self.called = True
        self.data = data

@pytest.fixture
def dummy_raw_data_service():
    return DummyRawDataService()

def test_process_message(monkeypatch, dummy_raw_data_service):
    monkeypatch.setattr(
        "app.consumers.consumer.raw_data_service.save_raw_data",
        dummy_raw_data_service.save_raw_data,
    )

    data = {"source": "test_source", "data": {"ID": "123", "STATUS": "OK"}}
    body = json.dumps(data).encode("utf-8")

    process_message(body)

    assert dummy_raw_data_service.called is True
    assert dummy_raw_data_service.data == data

class DummyChannel:
    def __init__(self):
        self.ack_called = False
        self.delivery_tag = None

    def basic_ack(self, delivery_tag):
        self.ack_called = True
        self.delivery_tag = delivery_tag

def test_callback(monkeypatch):
    monkeypatch.setattr("app.consumers.consumer.raw_data_service.save_raw_data", lambda data: None)

    dummy_channel = DummyChannel()
    dummy_method = type("DummyMethod", (), {"delivery_tag": "dummy_tag"})()
    dummy_properties = None
    body = json.dumps({"source": "test", "data": {"ID": "123"}}).encode("utf-8")

    callback(dummy_channel, dummy_method, dummy_properties, body)

    assert dummy_channel.ack_called is True
    assert dummy_channel.delivery_tag == "dummy_tag"
