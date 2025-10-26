import pika

from service.config.rabbit.queue_config import QUEUE_CONFIGS


def initialize_queues():
    for key, config in QUEUE_CONFIGS.items():
        credentials = pika.PlainCredentials(config["username"], config["password"])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config["host"],
                port=config["port"],
                credentials=credentials
            )
        )
        channel = connection.channel()

        channel.exchange_declare(
            exchange=config["exchange"],
            exchange_type=config["exchange_type"],
            durable=config["durable"]
        )

        channel.queue_declare(
            queue=config["queue_name"],
            durable=config["durable"]
        )

        channel.queue_bind(
            exchange=config["exchange"],
            queue=config["queue_name"],
            routing_key=config["routing_key"]
        )

        print(f"[init] Queue '{config['queue_name']}' bound to exchange '{config['exchange']}'")
        connection.close()
