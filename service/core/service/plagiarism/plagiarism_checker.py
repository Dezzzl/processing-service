from service.core.service.plagiarism.llm_plagiarism_checker import LLMPlagiarismChecker
from service.core.service.plagiarism.token_plagiarism_checker import TokenBasedPlagiarismChecker
import time
import logging

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

class PlagiarismChecker:
    """
    Гибридная система проверки на плагиат.
    1. Сначала токенизация и структурный анализ (алгоритм Морозова).
    2. При высоком проценте сходства — LLM-анализ для подтверждения/отклонения.
    """

    def __init__(
        self,
        lang_a: str = "python",
        lang_b: str = "python",
        token_threshold: float = 70.0,
    ):
        self.lang_a = lang_a
        self.lang_b = lang_b
        self.threshold = token_threshold
        self.logger = logging.getLogger(__name__)

        # Два токенайзера (для разных языков)
        self.token_checker = TokenBasedPlagiarismChecker(
            lang_a=self.lang_a,
            lang_b=self.lang_b,
            threshold=token_threshold,
        )

        # LLM — не зависит от языка напрямую, но можно указать в промпте
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
        llm_score = 0.0
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.logger.info(f"[INFO] Попытка {attempt}/{MAX_RETRIES} LLM...")
                llm_score = self.llm_checker.check(code_a, code_b)
                if llm_score is not None:
                    break
            except Exception as e:
                self.logger.warning(f"[WARN] Ошибка LLM на попытке {attempt}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)
        else:
            self.logger.error(f"[ERROR] LLM не дал ответ после {MAX_RETRIES} попыток")
            llm_score = 0.0

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
