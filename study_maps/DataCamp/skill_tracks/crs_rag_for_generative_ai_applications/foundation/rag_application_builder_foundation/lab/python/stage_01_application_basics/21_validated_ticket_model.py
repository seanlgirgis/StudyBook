"""Validate AI-generated ticket data before the application uses it."""

import json
from dataclasses import dataclass
from typing import Any

from rag_foundation.models.requests import TextGenerationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


@dataclass(frozen=True, slots=True)
class TicketTriage:
    """Validated support-ticket triage data."""

    category: str
    urgency: str
    summary: str
    next_action: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TicketTriage":
        """Create a ticket after validating AI-generated data."""

        required_fields = {
            "category",
            "urgency",
            "summary",
            "next_action",
        }

        missing_fields = required_fields - data.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Missing required fields: {missing}")

        unexpected_fields = data.keys() - required_fields
        if unexpected_fields:
            unexpected = ", ".join(sorted(unexpected_fields))
            raise ValueError(f"Unexpected fields: {unexpected}")

        for field_name in required_fields:
            value = data[field_name]

            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string.")

            if not value.strip():
                raise ValueError(f"{field_name} must not be blank.")

        allowed_urgencies = {"low", "medium", "high"}

        normalized_urgency = data["urgency"].strip().lower()
        if normalized_urgency not in allowed_urgencies:
            raise ValueError(
                "urgency must be low, medium, or high."
            )

        return cls(
            category=data["category"].strip(),
            urgency=normalized_urgency,
            summary=data["summary"].strip(),
            next_action=data["next_action"].strip(),
        )


customer_message = """
I was charged twice for my subscription this morning.
Please reverse the duplicate charge as soon as possible.
"""

provider = OpenAITextProvider(
    default_model="gpt-5.4-nano",
)

request = TextGenerationRequest(
    instructions=(
        "Triage the customer-support message. "
        "Return only valid JSON with exactly these fields: "
        "category, urgency, summary, next_action. "
        "Urgency must be low, medium, or high."
    ),
    prompt=customer_message,
    max_output_tokens=180,
)

result = provider.generate(request)

parsed_data = json.loads(result.require_text())
ticket = TicketTriage.from_dict(parsed_data)

print("VALIDATED SUPPORT TICKET")
print("------------------------")
print(f"Category: {ticket.category}")
print(f"Urgency: {ticket.urgency}")
print(f"Summary: {ticket.summary}")
print(f"Next action: {ticket.next_action}")
print()
print(f"Parsed type: {type(parsed_data).__name__}")
print(f"Validated type: {type(ticket).__name__}")