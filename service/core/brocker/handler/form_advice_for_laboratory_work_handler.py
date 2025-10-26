# service/core/brocker/handler/form_advice_for_lab_handler.py

from service.core.brocker.handler.handler import Handler
from service.core.model.event.form_advice_for_laboratory_work_event import FormAdviceForLaboratoryWorkEvent
from service.core.processor.form_advice_for_lab_processor import FormAdviceForLaboratoryWorkProcessor

class FormAdviceForLaboratoryWorkHandler(Handler):
    """
    Хендлер для события FormAdviceForLaboratoryWork
    """

    def __init__(self):
        self.processor = FormAdviceForLaboratoryWorkProcessor()

    def handle(self, payload: dict):
        event = FormAdviceForLaboratoryWorkEvent.from_dict(payload)
        print("Обрабатываем FormAdviceForLaboratoryWorkEvent:", event)
        result = self.processor.process(event)
        print(f"[INFO] Отправлено сообщение с рекомендацией: {result}")
