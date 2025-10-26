from service.core.brocker.handler.handler import Handler

class StudentSentLabHandler(Handler):
    def handle(self, payload: dict):
        print("Обрабатываем TASK:", payload)