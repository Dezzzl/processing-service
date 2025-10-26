from service.core.brocker.queue_names import QueueNames
from service.core.brocker.sender.rabbit_sender import RabbitSender
from service.core.client.minio_client import MinioClient
from service.core.model.event.form_advice_for_laboratory_work_event import FormAdviceForLaboratoryWorkEvent
from service.core.service.advice.llm_advice_generator import LLMAdviceGenerator


class FormAdviceForLaboratoryWorkProcessor:

    def __init__(self):
        self.minio_client = MinioClient()
        self.llm_checker = LLMAdviceGenerator()
        self.rabbit_sender = RabbitSender(QueueNames.PROCTORING_QUEUE)

    def process(self, event: FormAdviceForLaboratoryWorkEvent):
        file_for_advice = self.minio_client.get_file_by_id(event.file_key_id)
        lab_work_file = self.minio_client.get_file_by_id(event.lab_work_file_key_id)

        if not file_for_advice or not lab_work_file:
            return {"error": "Не удалось получить файлы из MinIO"}

        advice_str = self.llm_checker.get_advice(file_for_advice.decode(), lab_work_file.decode())

        self.rabbit_sender.send(
            {
                "type": "AdviceForLaboratoryWorkType",
                "payload": {
                    "chatId": event.chat_id,
                    "adviseStr": advice_str,
                },
            }
        )
