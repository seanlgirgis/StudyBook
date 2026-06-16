"""Use the shared library to generate and normalize text."""

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    prompt="In one sentence, explain why normalized AI responses are useful.",
    max_output_tokens=100,
)

result = provider.generate(request)

print("SHARED LIBRARY RESULT")
print("---------------------")
print(f"Text: {result.require_text()}")
print(f"Provider: {result.provider}")
print(f"Model: {result.model}")
print(f"Input tokens: {result.input_tokens}")
print(f"Output tokens: {result.output_tokens}")
print(f"Total tokens: {result.total_tokens}")
print(f"Request ID: {result.request_id}")
print(f"Result type: {type(result).__name__}")