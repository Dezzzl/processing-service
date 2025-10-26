from service.core.service.plagiarism.utils.compare import compare_codes
from service.core.service.plagiarism.utils.tokenizer import Tokenizer


class TokenBasedPlagiarismChecker:
    """
    Класс для проверки исходного кода на плагиат
    по алгоритму Морозова (токенизация + Хескел + Хиршберг)
    """

    def __init__(self, lang: str = "python", threshold: float = 70.0):
        self.lang = lang
        self.threshold = threshold
        self.tokenizer = Tokenizer(lang)

    def check(self, code_a: str, code_b: str) -> dict:
        """
        Проверка двух фрагментов исходного кода.
        :param code_a: исходный код №1 (строка)
        :param code_b: исходный код №2 (строка)
        :return: словарь с результатами проверки
        """
        tokens_a = self.tokenizer.tokenize(code_a)
        tokens_b = self.tokenizer.tokenize(code_b)

        result = compare_codes(tokens_a, tokens_b)

        return {
            **result,
            "average": result["average"],
            "is_plagiarism": result["average"] >= self.threshold,
            "lang": self.lang,
        }
