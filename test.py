from g4f.client import Client


class LLMPlagiarismChecker:
    def __init__(self, model_name: str = "deepseek-v3"):
        self.client = Client()
        self.model_name = model_name

    def check(self, prompt: str) -> str:
        print(self.client.models)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        # Получаем текст из ответа
        return response.choices[0].message.content


if __name__ == "__main__":
    llm_checker = LLMPlagiarismChecker()
    prompt = "Скажи кратко, что такое плагиат в программировании?"

    try:
        answer = llm_checker.check(prompt)
        print("Ответ модели:", answer)
    except Exception as e:
        print("Ошибка при вызове модели:", e)
