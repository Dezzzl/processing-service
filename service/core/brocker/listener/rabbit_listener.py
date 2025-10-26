# service/core/brocker/listner/rabbit_listener.py
import pika
import json
from service.config.rabbit.queue_config import get_queue_config
from service.core.brocker.handler.message_dispatcher import dispatch_message

class RabbitListener:
    def __init__(self, queue_key):
        self.config = get_queue_config(queue_key)

    def start_listening(self):
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
            try:
                message = json.loads(body)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Не удалось разобрать JSON: {e}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            try:
                dispatch_message(message)
            except Exception as e:
                print(f"[ERROR] Ошибка при обработке сообщения: {e}")
            finally:
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
