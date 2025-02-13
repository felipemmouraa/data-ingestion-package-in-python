# app/publishers/publisher.py
import json
import pika
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
        self.channel = self.connection.channel()
        # Ensure queues exist
        for q in settings.queue_names.values():
            self.channel.queue_declare(queue=q, durable=True)

    def publish(self, queue: str, message: dict):
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),  # persistent message
            )
            logger.info(f"Published message to {queue}")
        except Exception as e:
            logger.error(f"Failed to publish to {queue}: {str(e)}")

    def close(self):
        self.connection.close()

# Example usage (can be invoked periodically):
def publish_sample_messages():
    publisher = Publisher()
    try:
        # Simulate sending one message per queue
        for key, queue in settings.queue_names.items():
            sample_message = {"source": key, "data": {"ID": "2024-1422099", "STATUS": "R210", "STATUS_DATA": "2024-04-02-00.00.37.000000"}}
            publisher.publish(queue, sample_message)
    finally:
        publisher.close()
