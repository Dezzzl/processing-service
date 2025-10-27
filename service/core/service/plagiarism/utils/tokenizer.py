import json
import re
from pathlib import Path


class Tokenizer:
    """
    Универсальный токенизатор исходного кода для разных языков программирования.

    Использует словари токенов из папки:
    service/core/service/plagiarism/tokenizers/<language>.json

    Поддерживает:
    - ключевые слова
    - операторы
    - литералы (строки, числа)
    - идентификаторы
    """

    TOKENIZER_DIR = Path(__file__).parent.parent / "tokenizers"

    def __init__(self, language: str):
        self.language = language.lower()
        self.tokens = self._load_token_dictionary()
        self.patterns = self._build_patterns()

    # ---------------------------------------------------------
    # Инициализация токенов
    # ---------------------------------------------------------
    def _load_token_dictionary(self) -> dict:
        """Загружает словарь токенов для указанного языка, либо дефолтный (python)."""
        token_file = self.TOKENIZER_DIR / f"{self.language}.json"
        fallback_file = self.TOKENIZER_DIR / "python.json"

        if not token_file.exists():
            print(f"[WARN] Token dictionary for '{self.language}' not found, using fallback (python).")
            token_file = fallback_file

        with open(token_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_patterns(self) -> list[tuple[str, re.Pattern]]:
        """Создает список пар (токен, regex-паттерн)."""
        patterns = []
        for token_name, items in self.tokens.items():
            for item in sorted(items, key=len, reverse=True):  # длинные сначала
                # Если элемент состоит из букв/цифр — добавляем границы слова
                if re.match(r"^[A-Za-z_]+$", item):
                    regex = rf"\b{re.escape(item)}\b"
                else:
                    regex = re.escape(item)
                patterns.append((token_name, re.compile(regex)))
        return patterns

    # ---------------------------------------------------------
    # Токенизация
    # ---------------------------------------------------------
    def tokenize(self, code: str) -> list[str]:
        """
        Преобразует исходный код в последовательность токенов.
        Удаляет комментарии и строки, различает числа и идентификаторы.
        """
        # Удаляем комментарии и строки
        code = re.sub(r'".*?"|\'.*?\'', 'STRING_LITERAL', code)
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        tokens = []
        i = 0

        while i < len(code):
            match_found = False

            # Проверяем ключевые слова и операторы
            for token_name, regex in self.patterns:
                match = regex.match(code, i)
                if match:
                    tokens.append(token_name)
                    i = match.end()
                    match_found = True
                    break

            if not match_found:
                # Идентификаторы
                if re.match(r"[A-Za-z_]", code[i]):
                    ident = re.match(r"[A-Za-z_][A-Za-z0-9_]*", code[i:])
                    tokens.append("IDENTIFIER")
                    i += len(ident.group(0))
                # Числа
                elif re.match(r"\d", code[i]):
                    number = re.match(r"\d+(\.\d+)?", code[i:])
                    tokens.append("NUMBER")
                    i += len(number.group(0))
                else:
                    i += 1  # пропуск символа

        return tokens
