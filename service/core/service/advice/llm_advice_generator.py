from g4f.client import Client


class LLMAdviceGenerator:
    """
    Генератор рекомендаций по коду студента на основе задания лабораторной работы.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.client = Client()
        self.model_name = model_name

    def get_advice(self, student_code: str, lab_instruction: str) -> str:
        """
        Получает рекомендации для студента по его коду
        на основе текста задания лабораторной работы.
        """
        prompt = f"""
           Ты — преподаватель-программист. У студента есть решение лабораторной работы:

           ```python
           {student_code}
           ```

           Задание лабораторной работы:

           ```
           {lab_instruction}
           ```

           Проанализируй работу студента и составь краткую рецензию:
           - что сделано хорошо,
           - какие ошибки/проблемы есть,
           - как улучшить код и приблизить к требованию задания.

           Ответь только текстом, не используй JSON.
           """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return "Не удалось получить рекомендацию"