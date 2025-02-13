import pika
import json
from app.config import settings

class RabbitMQClient:
    def __init__(self):
        parameters = pika.URLParameters(settings.rabbitmq_url)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def publish_message(self, queue: str, message: dict) -> None:
        """
        Publish a message to the specified RabbitMQ queue.
        The message will be a JSON string.
        """
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )

    def __del__(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
