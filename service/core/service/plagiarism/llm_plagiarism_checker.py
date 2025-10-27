from g4f.client import Client

class LLMPlagiarismChecker:

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.client = Client()
        self.model_name = model_name

    def check(self, code_a: str, code_b: str) -> float:
        prompt = f"""
        Ты — эксперт по анализу программного кода.
        Твоя задача — определить, насколько два фрагмента кода похожи по логике (а не по синтаксису).

        Код A:
        ```
        {code_a}
        ```

        Код B:
        ```
        {code_b}
        ```

        Дай ответ строго в формате JSON(Только json и ничего больше):
        {{
            "similarity": <число от 0 до 1>,
            "reason": "<краткое объяснение>"
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )

        print(response)

        try:
            raw_text = response.choices[0].message.content
            print("[INFO] Answer from LLM about plagiarism: " + raw_text)
            import json
            data = json.loads(raw_text)
            return float(data.get("similarity", 0.0))
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return 0.0
