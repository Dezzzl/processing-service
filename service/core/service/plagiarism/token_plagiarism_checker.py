from service.core.service.plagiarism.utils.compare import compare_codes
from service.core.service.plagiarism.utils.tokenizer import Tokenizer


class TokenBasedPlagiarismChecker:
    """
    Класс для проверки исходного кода на плагиат
    по алгоритму Морозова (токенизация + сравнение по токенам).
    Теперь поддерживает сравнение кода на разных языках.
    """

    def __init__(self, lang_a: str = "python", lang_b: str = "python", threshold: float = 50.0):
        self.lang_a = lang_a
        self.lang_b = lang_b
        self.threshold = threshold

        # Два токенайзера — для каждого языка свой
        self.tokenizer_a = Tokenizer(lang_a)
        self.tokenizer_b = Tokenizer(lang_b)

    def check(self, code_a: str, code_b: str) -> dict:
        """
        Проверка двух фрагментов исходного кода.
        :param code_a: исходный код №1 (например, Python)
        :param code_b: исходный код №2 (например, C++)
        :return: словарь с результатами проверки
        """
        tokens_a = self.tokenizer_a.tokenize(code_a)
        tokens_b = self.tokenizer_b.tokenize(code_b)

        result = compare_codes(tokens_a, tokens_b)

        return {
            **result,
            "average": result["average"],
            "is_plagiarism": result["average"] >= self.threshold,
            "lang_a": self.lang_a,
            "lang_b": self.lang_b,
            "token_count_a": len(tokens_a),
            "token_count_b": len(tokens_b),
        }