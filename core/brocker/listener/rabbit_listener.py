import pika
import json
from config.rabbit.queue_config import get_queue_config

class RabbitListener:
    def __init__(self, queue_key):
        self.config = get_queue_config(queue_key)

    def start_listening(self, callback):
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

        print(f"[*] Listening on '{self.config['queue_name']}'...")

        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=self.config["prefetch_count"])
        channel.basic_consume(queue=self.config["queue_name"], on_message_callback=on_message)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopped listening.")
            channel.stop_consuming()
        finally:
            connection.close()
