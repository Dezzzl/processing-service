import json
import re
from pathlib import Path


class Tokenizer:
    def __init__(self, language: str):
        token_file = Path(__file__).parent.parent / "tokenizers" / f"{language}.json"
        if not token_file.exists():
            raise ValueError(f"Token dictionary for {language} not found.")
        with open(token_file, "r", encoding="utf-8") as f:
            self.tokens = json.load(f)

    def tokenize(self, code: str) -> list[str]:
        """
        Преобразует исходный код в последовательность токенов на основе словаря.
        Поддерживает ключевые слова, операторы и идентификаторы (переменные, функции).
        """
        token_sequence = []

        # 1. Заменяем все фиксированные ключевые слова и операторы на их токены
        for token_name, patterns in self.tokens.items():
            for pattern in patterns:
                escaped_pattern = re.escape(pattern)
                code = re.sub(rf"\b{escaped_pattern}\b", token_name, code)

        # 2. Находим все слова в коде
        words = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)

        for w in words:
            if w in self.tokens:  # если это ключевой токен
                token_sequence.append(w)
            else:
                token_sequence.append("IDENTIFIER")  # иначе это идентификатор

        return token_sequence
