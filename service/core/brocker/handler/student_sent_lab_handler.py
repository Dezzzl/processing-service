from service.core.brocker.handler.handler import Handler
from service.core.model.event.student_sent_lab_event import StudentSentLabEvent
from service.core.processor.student_sent_lab_processor import PlagiarismProcessor


class StudentSentLabHandler(Handler):
    def __init__(self):
        self.processor = PlagiarismProcessor()

    def handle(self, payload: dict):
        event = StudentSentLabEvent.from_dict(payload)
        print("Обрабатываем StudentSentLabEvent:", event)
        self.processor.process_event(event)