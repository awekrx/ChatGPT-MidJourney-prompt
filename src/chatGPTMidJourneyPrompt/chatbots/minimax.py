import os

from openai import OpenAI

MINIMAX_API_BASE = "https://api.minimax.io/v1"
MINIMAX_DEFAULT_MODEL = "MiniMax-M2.7"
_MINIMAX_TEMP_MIN = 0.01
_MINIMAX_TEMP_MAX = 1.0


class ChatbotMiniMax:
    """MiniMax LLM backend using the OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        model: str = MINIMAX_DEFAULT_MODEL,
        temperature: float = 0.7,
    ):
        self.client = OpenAI(api_key=api_key, base_url=MINIMAX_API_BASE)
        self.model = model
        # MiniMax temperature must be in (0.0, 1.0]
        self.temperature = max(_MINIMAX_TEMP_MIN, min(_MINIMAX_TEMP_MAX, temperature))

    def ask(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content
