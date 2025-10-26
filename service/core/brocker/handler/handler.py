# service/core/brocker/handlers/base_handler.py
class Handler:
    def handle(self, payload: dict):
        """Метод, который реализует обработку конкретного payload"""
        raise NotImplementedError("handle() должен быть реализован в наследнике")
