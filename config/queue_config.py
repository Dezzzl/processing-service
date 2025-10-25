import yaml
from core.brocker.queue_names import QueueNames

with open("config.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

CONNECTION_CONFIG = yaml_data["connection"]
QUEUES_CONFIG = yaml_data["queues"]

QUEUE_CONFIGS = {
    QueueNames.TASK_QUEUE: {**CONNECTION_CONFIG, **QUEUES_CONFIG["task_queue"]},
    QueueNames.NOTIFICATION_QUEUE: {**CONNECTION_CONFIG, **QUEUES_CONFIG["notification_queue"]},
}

def get_queue_config(queue_key):
    return QUEUE_CONFIGS[queue_key]
