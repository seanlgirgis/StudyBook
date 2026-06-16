from dataclasses import dataclass


@dataclass(frozen=True)
class RequestOptions:
    temperature: float = 0.0
    max_tokens: int | None = None