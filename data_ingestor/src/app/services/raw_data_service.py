# app/services/raw_data_service.py
import io
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import boto3
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

def save_raw_data(data: dict) -> None:
    """
    Saves raw data into a parquet file and uploads it to Supabase storage (S3 compatible).
    The file will be stored in a bucket defined in your settings under a folder named after the data source.
    """
    try:
        source = data.get("source", "default")
        # Convert payload to a DataFrame.
        df = pd.DataFrame([data.get("data", {})])
        # Convert DataFrame to an Apache Arrow Table.
        table = pa.Table.from_pandas(df)
        
        # Write the table to an in-memory bytes buffer.
        buffer = io.BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)

        file_key = f"{source}/raw_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.parquet"

        s3_client = boto3.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            region_name=settings.region_name,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        bucket_name = settings.supabase_bucket  
        s3_client.upload_fileobj(buffer, bucket_name, file_key)
        
        logger.info(f"Raw data uploaded to bucket {bucket_name} as {file_key}")
    except Exception as e:
        logger.error(f"Error saving raw data: {str(e)}")
        raise e
