from flask import Flask, request, jsonify
import threading
from config.rabbit.rabbit_initializer import initialize_queues
from core.brocker.listener.rabbit_listener import RabbitListener
from core.brocker.sender.rabbit_sender import RabbitSender
from config.rabbit.queue_config import QueueNames

app = Flask(__name__)

initialize_queues()

def handle_message(msg):
    print(f"[Listener] Получено сообщение: {msg}")

def start_listener():
    listener = RabbitListener(QueueNames.TASK_QUEUE)
    listener.start_listening(handle_message)

listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()
print("[Main] Listener запущен в отдельном потоке.")

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    sender = RabbitSender(QueueNames.TASK_QUEUE)
    sender.send(data)
    return jsonify({"status": "Message sent", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
