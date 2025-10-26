from minio import Minio
from service.config.minio.minio_config import get_minio_config

def get_minio_client():
    cfg = get_minio_config()

    client = Minio(
        cfg["endpoint"],
        access_key=cfg["access_key"],
        secret_key=cfg["secret_key"],
        secure=cfg.get("secure", False)
    )
    return client
