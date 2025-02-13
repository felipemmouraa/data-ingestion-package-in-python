# app/services/transformation_service.py
from datetime import datetime
import pandas as pd
from clickhouse_driver import Client
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

def transform_data(data: dict) -> dict:
    """
    Applies a transformation to the raw data.
    In this example, we lowercase keys and add an ingestion timestamp.
    
    :param data: The raw data dictionary containing a 'data' key.
    :return: A dictionary with transformed data.
    """
    try:
        transformed = {k.lower(): v for k, v in data.get("data", {}).items()}
        transformed["ingested_at"] = datetime.utcnow().isoformat()
        return transformed
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise e

def transform_and_save(data: dict) -> None:
    """
    Transforms raw data and inserts it into a ClickHouse table.
    
    :param data: Raw data with a "source" key to identify which table to target.
    """
    try:
        # Transform the data.
        transformed = transform_data(data)
        
        # Map raw source to a ClickHouse table name.
        table_mapping = {
            "raw_data_1": "table1",
            "raw_data_2": "table2",
            "raw_data_3": "table3",
            "raw_data_4": "table4",
        }
        source = data.get("source", "raw_data_1")
        table_name = table_mapping.get(source, "default_table")
        
        # For demonstration, create a DataFrame with a single row.
        df = pd.DataFrame([transformed])
        
        # Prepare to insert into ClickHouse.
        client = Client.from_url(settings.clickhouse_url)
        records = [tuple(row) for row in df.to_numpy()]
        columns = list(df.columns)
        insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES"
        
        # Execute the insert query.
        client.execute(insert_query, records)
        logger.info(f"Transformed data inserted into {table_name}")
    except Exception as e:
        logger.error(f"Error in transform_and_save: {str(e)}")
        raise e
