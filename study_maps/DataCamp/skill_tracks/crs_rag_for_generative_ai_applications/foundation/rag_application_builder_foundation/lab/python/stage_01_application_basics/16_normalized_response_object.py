"""Demonstrate converting an OpenAI response into our own response object."""

from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class AIResponse:
    """Provider-independent response returned to the application."""

    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    request_id: str | None


client = OpenAI()

raw_response = client.responses.create(
    model="gpt-5.4-nano",
    input="In one sentence, explain what application routing means.",
)

normalized_response = AIResponse(
    text=raw_response.output_text,
    provider="openai",
    model=raw_response.model,
    input_tokens=raw_response.usage.input_tokens,
    output_tokens=raw_response.usage.output_tokens,
    request_id=raw_response.id,
)

print("AI RESPONSE")
print("-----------")
print(f"Text: {normalized_response.text}")
print(f"Provider: {normalized_response.provider}")
print(f"Model: {normalized_response.model}")
print(f"Input tokens: {normalized_response.input_tokens}")
print(f"Output tokens: {normalized_response.output_tokens}")
print(f"Request ID: {normalized_response.request_id}")