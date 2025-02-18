# app/services/raw_data_service.py
import io
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from supabase import create_client
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

supabase = create_client(settings.supabase_url, settings.supabase_key)

def save_raw_data(data: dict) -> None:
    """
    Saves raw data into a parquet file and uploads it to Supabase Storage.
    Inserts metadata into the parquet_metadata table.
    """
    try:
        source = data.get("source", "default")
        df = pd.DataFrame([data.get("data", {})])
        table = pa.Table.from_pandas(df)

        buffer = io.BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)

        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        file_path = f"{source}/raw_{timestamp}.parquet"
        bucket_name = settings.supabase_bucket  

        response = supabase.storage.from_(bucket_name).upload(
            file_path,
            buffer.getvalue(), 
            file_options={"content-type": "application/octet-stream"}
        )

        classification_id = get_classification_for_source(source)

        try:
            logger.info("Attempting to insert metadata into parquet_metadata table")
            response = supabase.table("parquet_metadata").insert({
                "bucket": bucket_name,
                "file_path": file_path,
                "classification_id": classification_id,
            }).execute()

            logger.info(f"Supabase insert response: {response}")

        except Exception as e:
            logger.info(f"Error inserting metadata: {str(e)}")

        logger.info(f"teste {response}")
        logger.info(f"Raw data uploaded to bucket {bucket_name} as {file_path}")

    except Exception as e:
        logger.error(f"Error saving raw data: {str(e)}")
        raise e

def get_classification_for_source(source: str) -> int:
    """
    Returns classification ID based on the data source.
    """
    classifications = {
        "raw_data_1": 1,  
        "raw_data_2": 1,  
        "raw_data_3": 1,  
        "raw_data_4": 1   
    }
    return classifications.get(source, 1)  

