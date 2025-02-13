# app/consumers/consumer.py
import json
import pika
from threading import Thread
from app.config import settings
from app.services import raw_data_service, transformation_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

def process_message(body: bytes):
    try:
        data = json.loads(body)
        # Save raw data to Supabase (as Parquet) and trigger transformation.
        raw_data_service.save_raw_data(data)
        # transformation_service.transform_and_save(data)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

def callback(ch, method, properties, body):
    logger.info("Received message")
    process_message(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer(queue_name: str):
    connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    logger.info(f"Started consumer on queue {queue_name}")
    channel.start_consuming()

def start_all_consumers():
    threads = []
    for queue in settings.queue_names.values():
        thread = Thread(target=start_consumer, args=(queue,), daemon=True)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
