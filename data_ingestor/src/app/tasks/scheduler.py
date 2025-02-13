# app/tasks/scheduler.py
import asyncio
from app.publishers.publisher import publish_sample_messages
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def periodic_publisher(interval: int = 30):
    while True:
        logger.info("Publishing sample messages")
        publish_sample_messages()
        await asyncio.sleep(interval)
