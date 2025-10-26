import os

import yaml
from service.core.brocker.queue_names import QueueNames
from service.core.utils.constants import PROJECT_ROOT

config_path = os.path.join(PROJECT_ROOT, "config.yaml")

with open(config_path, "r") as f:
    yaml_data = yaml.safe_load(f)

CONNECTION_CONFIG = yaml_data["connection"]
QUEUES_CONFIG = yaml_data["queues"]

QUEUE_CONFIGS = {
    QueueNames.PROCTORING_QUEUE: {**CONNECTION_CONFIG, **QUEUES_CONFIG["proctoring_queue"]}
}

def get_queue_config(queue_key):
    return QUEUE_CONFIGS[queue_key]
