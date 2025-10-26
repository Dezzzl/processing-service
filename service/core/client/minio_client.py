from service.config.minio.minio_client import get_minio_client
from service.config.minio.minio_config import get_minio_config
from minio.error import S3Error

class MinioClient:
    def __init__(self):
        """Создание клиента MinIO с параметрами из конфигурации"""
        self.config = get_minio_config()
        self.client = get_minio_client()
        self.bucket = self.config["bucket"]

        # Проверяем, что бакет существует
        if not self.client.bucket_exists(self.bucket):
            print(f"Бакет '{self.bucket}' не найден. Создаю...")
            self.client.make_bucket(self.bucket)

    def get_file_by_id(self, file_id: str) -> bytes:
        """Получает файл по ID (object_name) из MinIO и возвращает содержимое"""
        try:
            response = self.client.get_object(self.bucket, file_id)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            print(f"Ошибка при получении файла '{file_id}': {e}")
            return None