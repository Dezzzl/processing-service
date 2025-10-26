import os


from service.core.brocker.queue_names import QueueNames
from service.core.brocker.sender.rabbit_sender import RabbitSender
from service.core.client.minio_client import MinioClient
from service.core.model.event.student_sent_lab_event import StudentSentLabEvent
from service.core.service.plagiarism.plagiarism_checker import PlagiarismChecker


class PlagiarismProcessor:
    """
    Основной процессор проверки лабораторных работ на плагиат.
    Работает по алгоритму из PlantUML-сценария.
    """

    # Расширения → язык
    EXTENSION_TO_LANG = {
        ".py": "python",
        ".java": "java",
        ".cs": "csharp",
        ".cpp": "cpp",
        ".c": "c",
        ".js": "javascript",
    }

    def __init__(self):
        self.minio = MinioClient()
        self.result_sender = RabbitSender(QueueNames.PROCTORING_QUEUE)

    def process_event(self, event: StudentSentLabEvent):
        print(f"[INFO] Начата обработка лабораторной работы для chatId={event.chat_id}")

        # Получаем основной файл
        file_for_check = self.minio.get_file_by_id(event.file_key_id)
        if not file_for_check:
            print(f"[ERROR] Не удалось получить файл для проверки: {event.file_key_id}")
            return

        file_for_check = file_for_check.decode("utf-8")

        # Определяем язык по расширению
        lang = self._detect_language(event.file_key_id)
        print(f"[INFO] Определён язык исходного файла: {lang}")

        plagiarism_checker = PlagiarismChecker(lang=lang)

        # Проверяем против других файлов предмета
        for suspect_key in event.same_subject_files_key_ids:
            print(f"[DEBUG] Проверяем с файлом: {suspect_key}")
            suspect_data = self.minio.get_file_by_id(suspect_key)

            if not suspect_data:
                print(f"[WARN] Не удалось получить файл {suspect_key}, пропускаем.")
                continue

            suspect_code = suspect_data.decode("utf-8")

            result = plagiarism_checker.check(file_for_check, suspect_code)

            if result["is_plagiarism"]:
                print(f"[ALERT] Найден плагиат: {event.file_key_id} ↔ {suspect_key}")
                self._send_plagiarism_found(event, suspect_key)
                return

        print(f"[INFO] Плагиат не найден для {event.file_key_id}")
        self._send_plagiarism_not_found(event)

    def _detect_language(self, file_key: str) -> str:
        """Определяет язык программирования по расширению файла"""
        _, ext = os.path.splitext(file_key)
        return self.EXTENSION_TO_LANG.get(ext.lower(), "python")  # по умолчанию Python

    def _send_plagiarism_found(self, event: StudentSentLabEvent, plagiarism_file_key: str):
        message = {
            "chatId": event.chat_id,
            "decision": "PLAGIARISM_FOUND",
            "plagiarismFileKeyId": plagiarism_file_key,
        }
        self.result_sender.send(message)
        print(f"[INFO] Отправлено сообщение о найденном плагиате: {message}")

    def _send_plagiarism_not_found(self, event: StudentSentLabEvent):
        message = {
            "chatId": event.chat_id,
            "decision": "PLAGIARISM_NOT_FOUND",
            "plagiarismFileKeyId": event.file_key_id,
            "labWorkLink": f"https://minio/labworks/{event.lab_work_file_key_id}",
        }
        self.result_sender.send(message)
        print(f"[INFO] Отправлено сообщение об отсутствии плагиата: {message}")
