import yaml
import os

from service.core.utils.constants import PROJECT_ROOT


def get_minio_config():
    """Читает конфигурацию MinIO из application.yml"""
    config_path = os.path.join(PROJECT_ROOT, "config.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config["minio"]