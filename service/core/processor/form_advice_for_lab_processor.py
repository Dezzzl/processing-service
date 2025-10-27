from service.core.brocker.queue_names import QueueNames
from service.core.brocker.sender.rabbit_sender import RabbitSender
from service.core.client.minio_client import MinioClient
from service.core.model.event.form_advice_for_laboratory_work_event import FormAdviceForLaboratoryWorkEvent
from service.core.service.advice.llm_advice_generator import LLMAdviceGenerator

import time
import logging

MAX_RETRIES = 3          # максимальное число попыток
RETRY_DELAY_SECONDS = 2  # задержка между попытками

class FormAdviceForLaboratoryWorkProcessor:

    def __init__(self):
        self.minio_client = MinioClient()
        self.llm_checker = LLMAdviceGenerator()
        self.rabbit_sender = RabbitSender(QueueNames.PROCTORING_QUEUE)
        self.logger = logging.getLogger(__name__)

    def process(self, event: FormAdviceForLaboratoryWorkEvent):
        file_for_advice = self.minio_client.get_file_by_id(event.file_key_id)
        lab_work_file = self.minio_client.get_file_by_id(event.lab_work_file_key_id)

        if not file_for_advice or not lab_work_file:
            return {"error": "Не удалось получить файлы из MinIO"}

        file_for_advice = file_for_advice.decode()
        lab_work_file = lab_work_file.decode()

        advice_str = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.logger.info(f"[INFO] Попытка {attempt}/{MAX_RETRIES} получить совет от LLM...")
                advice_str = self.llm_checker.get_advice(file_for_advice, lab_work_file)
                if advice_str and advice_str.strip():
                    break  # успех, выходим из цикла
            except Exception as e:
                self.logger.warning(f"[WARN] Ошибка LLM на попытке {attempt}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)

        if not advice_str:
            self.logger.error(f"[ERROR] LLM не смог сгенерировать ответ после {MAX_RETRIES} попыток")
            advice_str = "⚠️ Не удалось сформировать рекомендацию. Попробуйте позже."

        self.rabbit_sender.send(
            {
                "type": "AdviceForLaboratoryWorkType",
                "payload": {
                    "chatId": event.chat_id,
                    "adviseStr": advice_str,
                },
            }
        )
