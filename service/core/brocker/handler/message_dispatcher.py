from .form_advice_for_laboratory_work_handler import FormAdviceForLaboratoryWorkHandler
from .student_sent_lab_handler import StudentSentLabHandler

MESSAGE_HANDLERS = {
    "StudentSentLabType": StudentSentLabHandler(),
    "FormAdviceForLaboratoryWorkType": FormAdviceForLaboratoryWorkHandler()
}

def dispatch_message(message: dict):
    message_type = message.get("messageType")
    payload = message.get("payload", {})

    handler = MESSAGE_HANDLERS.get(message_type)
    if handler:
        print(f"[INFO] Начата обработка сообщения для messageType: {message_type} с payload: {payload}")
        handler.handle(payload)
    else:
        print(f"[WARN] Нет обработчика для messageType: {message_type}")
