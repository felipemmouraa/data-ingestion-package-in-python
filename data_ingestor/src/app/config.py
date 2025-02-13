import os

class Settings:
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    supabase_db_url: str = os.getenv("SUPABASE_DB_URL", "postgresql://username:password@db.supabase.co:5432/dbname")
    supabase_url: str = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
    supabase_key: str = os.getenv("SUPABASE_KEY", "your_supabase_key")
    queue_names: dict = {
        "raw_data_1": "queue_raw_1",
        "raw_data_2": "queue_raw_2",
        "raw_data_3": "queue_raw_3",
        "raw_data_4": "queue_raw_4",
    }
    endpoint_url: str = os.getenv("STORAGE_ENDPOINT", "https://your-bucket.s3.region.amazonaws.com")
    region_name: str = os.getenv("STORAGE_REGION", "us-east-1")
    aws_access_key_id: str = os.getenv("ACCESS_KEY_ID_STORAGE", "your_access_key_id")
    aws_secret_access_key: str = os.getenv("SECRET_ACCESS_KEY_STORAGE", "your_secret_access_key")
    supabase_bucket: str = os.getenv("SUPABASE_BUCKET", "your_bucket_name")

settings = Settings()
