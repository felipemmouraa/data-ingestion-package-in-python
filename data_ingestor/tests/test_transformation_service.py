import pytest
from app.services.transformation_service import transform_data

def test_transform_data():
    raw_data = {"data": {"ID": "123", "STATUS": "OK", "Extra": "value"}}
    transformed = transform_data(raw_data)

    assert "id" in transformed
    assert "status" in transformed
    assert "extra" in transformed
    assert "ingested_at" in transformed
