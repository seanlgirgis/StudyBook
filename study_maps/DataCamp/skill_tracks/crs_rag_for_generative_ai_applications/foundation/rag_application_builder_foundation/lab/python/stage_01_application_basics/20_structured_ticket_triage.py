"""Convert a support message into structured application data."""

import json

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


customer_message = """
I was charged twice for my subscription this morning.
Please reverse the duplicate charge as soon as possible.
"""

provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    instructions=(
        "You triage customer-support messages. "
        "Return only valid JSON with these exact fields: "
        "category, urgency, summary, next_action. "
        "Do not include markdown fences or additional commentary."
    ),
    prompt=customer_message,
    max_output_tokens=180,
)

result = provider.generate(request)

raw_text = result.require_text()
ticket = json.loads(raw_text)

print("STRUCTURED SUPPORT TICKET")
print("-------------------------")
print(f"Category: {ticket['category']}")
print(f"Urgency: {ticket['urgency']}")
print(f"Summary: {ticket['summary']}")
print(f"Next action: {ticket['next_action']}")
print()
print(f"Result type: {type(result).__name__}")
print(f"Parsed type: {type(ticket).__name__}")
print(f"Total tokens: {result.total_tokens}")