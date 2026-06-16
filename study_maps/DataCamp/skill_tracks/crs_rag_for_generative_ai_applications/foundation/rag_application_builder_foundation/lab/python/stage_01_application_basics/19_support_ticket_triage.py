"""Triage a customer-support message using the shared AI provider."""

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


customer_message = """
I was charged twice for my subscription this morning.
I need the duplicate charge reversed as soon as possible.
"""

provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    instructions=(
        "You triage customer-support messages. "
        "Return exactly four labeled lines: "
        "Category, Urgency, Summary, Next action."
    ),
    prompt=customer_message,
    max_output_tokens=180,
)

result = provider.generate(request)

print("SUPPORT TICKET TRIAGE")
print("---------------------")
print(result.require_text())
print()
print(f"Provider: {result.provider}")
print(f"Model: {result.model}")
print(f"Total tokens: {result.total_tokens}")