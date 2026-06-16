"""Use separate instructions and user prompt through the shared provider."""

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    instructions=(
        "You are a technical tutor. "
        "Use plain language and answer in exactly two bullet points."
    ),
    prompt="Explain why an application should use a shared AI provider library.",
    max_output_tokens=120,
)

result = provider.generate(request)

print("INSTRUCTIONS + PROMPT")
print("---------------------")
print(result.require_text())
print()
print(f"Model: {result.model}")
print(f"Total tokens: {result.total_tokens}")