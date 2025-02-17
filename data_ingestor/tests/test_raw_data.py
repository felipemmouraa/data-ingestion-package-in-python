import io
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from app.services import raw_data_service

class DummyS3Client:
    def __init__(self):
        self.uploads = []

    def upload_fileobj(self, fileobj, bucket, key):
        self.uploads.append((bucket, key))

def dummy_boto3_client(*args, **kwargs):
    return DummyS3Client()

def test_save_raw_data(monkeypatch):
    dummy_s3 = DummyS3Client()
    monkeypatch.setattr(raw_data_service, "boto3", type("dummy", (), {"client": lambda *args, **kwargs: dummy_s3}))

    sample_data = {"source": "test_source", "data": {"ID": "123", "STATUS": "OK"}}

    raw_data_service.save_raw_data(sample_data)

    assert len(dummy_s3.uploads) == 1
    bucket, key = dummy_s3.uploads[0]

    from app.config import settings
    assert bucket == settings.supabase_bucket
