import pika
import json
from config.queue_config import get_queue_config

class RabbitSender:
    def __init__(self, queue_key):
        self.config = get_queue_config(queue_key)

    def send(self, message: dict):
        credentials = pika.PlainCredentials(
            self.config["username"], self.config["password"]
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config["host"],
                port=self.config["port"],
                virtual_host=self.config.get("virtual_host", "/"),
                credentials=credentials
            )
        )
        channel = connection.channel()

        channel.basic_publish(
            exchange=self.config["exchange"],
            routing_key=self.config["routing_key"],
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[→] Sent message to '{self.config['queue_name']}': {message}")
        connection.close()
