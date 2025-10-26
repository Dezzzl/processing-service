from flask import Flask, request, jsonify
import threading
from service.config.rabbit.rabbit_initializer import initialize_queues
from service.core.brocker.listener.rabbit_listener import RabbitListener
from service.core.brocker.sender.rabbit_sender import RabbitSender
from service.core.brocker.queue_names import QueueNames
from service.core.client.minio_client import MinioClient

app = Flask(__name__)

initialize_queues()

def start_listener():
    listener = RabbitListener(QueueNames.PROCESSING_SERVICE_QUEUE)
    listener.start_listening()

listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()
print("[Main] Listener запущен в отдельном потоке.")

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    sender = RabbitSender(QueueNames.PROCTORING_QUEUE)
    sender.send(data)
    return jsonify({"status": "Message sent", "data": data})


if __name__ == "__main__":
    client = MinioClient()
    data = client.get_file_by_id("subject.labwork.123.zip")

    if data:
        print("Файл успешно получен, размер:", len(data))
    app.run(host="0.0.0.0", port=5000, debug=True)
