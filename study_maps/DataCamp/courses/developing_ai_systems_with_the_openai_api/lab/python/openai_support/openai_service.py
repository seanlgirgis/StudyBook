import os
from collections.abc import Sequence

from openai import OpenAI

from .message import Message
from .request_options import RequestOptions


class OpenAIService:
    """Encapsulates OpenAI client and request plumbing."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        self._client = OpenAI(api_key=api_key)
        self._model = model

    def get_response(
        self,
        prompt: str | None = None,
        messages: Sequence[Message] | None = None,
        options: RequestOptions | None = None,
    ) -> str:
        if prompt is None and messages is None:
            raise ValueError("Provide either prompt or messages.")

        if prompt is not None and messages is not None:
            raise ValueError("Provide prompt or messages, not both.")

        if prompt is not None:
            messages = [
                Message(
                    role="user",
                    content=prompt,
                )
            ]

        options = options or RequestOptions()

        request: dict = {
            "model": self._model,
            "messages": [
                message.to_dict()
                for message in messages or []
            ],
            "temperature": options.temperature,
        }

        if options.max_tokens is not None:
            request["max_tokens"] = options.max_tokens

        response = self._client.chat.completions.create(**request)

        return response.choices[0].message.content or ""