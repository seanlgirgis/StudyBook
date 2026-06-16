"""Demonstrate how the output-token limit affects completion."""

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    instructions=(
        "You are a technical tutor. "
        "Use plain language and answer in exactly two short bullet points."
    ),
    prompt="Explain why an application should use a shared AI provider library.",
    max_output_tokens=220,
)

result = provider.generate(request)

print("LARGER OUTPUT LIMIT")
print("-------------------")
print(result.require_text())
print()
print(f"Input tokens: {result.input_tokens}")
print(f"Output tokens: {result.output_tokens}")
print(f"Total tokens: {result.total_tokens}")