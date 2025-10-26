from service.core.service.plagiarism.llm_plagiarism_checker import LLMPlagiarismChecker
from service.core.service.plagiarism.token_plagiarism_checker import TokenBasedPlagiarismChecker


class PlagiarismChecker:
    """
    Гибридная система проверки на плагиат.
    1. Сначала токенизация и структурный анализ (алгоритм Морозова).
    2. При высоком проценте сходства — LLM-анализ для подтверждения/отклонения.
    """

    def __init__(self, lang: str = "python", token_threshold: float = 70.0):
        self.threshold = token_threshold
        self.lang = lang
        self.token_checker = TokenBasedPlagiarismChecker(lang=lang, threshold=token_threshold)
        self.llm_checker = LLMPlagiarismChecker()

    def check(self, code_a: str, code_b: str) -> dict:
        """
        Запускает гибридную проверку двух фрагментов кода.
        :param code_a: исходный код №1
        :param code_b: исходный код №2
        :return: результат проверки с объединёнными метриками
        """
        # Шаг 1 — базовая токен-проверка
        token_result = self.token_checker.check(code_a, code_b)

        # Если базовый результат ниже порога — сразу возвращаем
        if not token_result["is_plagiarism"]:
            return {
                "method": "token",
                "average": token_result["average"],
                "is_plagiarism": False,
                "llm_used": False,
                "details": token_result,
            }

        # Шаг 2 — уточняем результат с помощью LLM
        llm_score = self.llm_checker.check(code_a, code_b)  # float 0-100

        # Определяем финальное решение по LLM-порогам
        final_decision = llm_score >= self.threshold / 100

        return {
            "method": "hybrid",
            "token_score": token_result["average"],
            "llm_score": llm_score,
            "is_plagiarism": final_decision,
            "llm_used": True,
            "details": {
                "token_result": token_result,
                "llm_score": llm_score,
            },
        }
