"""Stage 1, Brick 40: Extract and validate structured fields.

Functionality studied:
    Extract specific facts from unstructured text and convert them into
    validated application data.

Reusable mechanics:
    - TextGenerationRequest
    - OpenAITextProvider
    - parse_json_object()

Application-specific behavior:
    - required field names;
    - allowed priority values;
    - field validation rules.
"""

from dataclasses import dataclass

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.structured import parse_json_object


SOURCE_TEXT = """
Maria Lopez from Northwind Traders reported that invoice INV-4087 was
charged twice. She needs the duplicate charge investigated before Friday.
The issue should be treated as high priority.
""".strip()


@dataclass
class InvoiceIssue:
    """Validated invoice information extracted from text."""

    customer_name: str
    company: str
    invoice_number: str
    issue: str
    deadline: str
    priority: str

    @classmethod
    def from_dict(cls, data: dict) -> "InvoiceIssue":
        """Create a validated InvoiceIssue from parsed JSON."""

        required_fields = {
            "customer_name",
            "company",
            "invoice_number",
            "issue",
            "deadline",
            "priority",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing_text = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Missing required fields: {missing_text}"
            )

        unexpected_fields = data.keys() - required_fields

        if unexpected_fields:
            unexpected_text = ", ".join(
                sorted(unexpected_fields)
            )
            raise ValueError(
                f"Unexpected fields: {unexpected_text}"
            )

        cleaned_values = {}

        for field_name in required_fields:
            value = data[field_name]

            if not isinstance(value, str):
                raise TypeError(
                    f"{field_name} must be a string."
                )

            cleaned_value = value.strip()

            if cleaned_value == "":
                raise ValueError(
                    f"{field_name} must not be blank."
                )

            cleaned_values[field_name] = cleaned_value

        allowed_priorities = {
            "low",
            "medium",
            "high",
        }

        priority = cleaned_values["priority"].lower()

        if priority not in allowed_priorities:
            raise ValueError(
                "priority must be low, medium, or high."
            )

        cleaned_values["priority"] = priority

        return cls(**cleaned_values)


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Extract information from the supplied text. "
            "Return valid JSON only with exactly these fields: "
            "customer_name, company, invoice_number, issue, "
            "deadline, and priority. "
            "Priority must be low, medium, or high. "
            "Do not add fields or infer missing facts."
        ),
        prompt=SOURCE_TEXT,
        model="gpt-5.4-nano",
    )

    result = provider.generate(request)

    parsed_data = parse_json_object(
        result.require_text()
    )

    issue = InvoiceIssue.from_dict(parsed_data)

    print("VALIDATED EXTRACTION")
    print("--------------------")
    print(f"Customer: {issue.customer_name}")
    print(f"Company: {issue.company}")
    print(f"Invoice: {issue.invoice_number}")
    print(f"Issue: {issue.issue}")
    print(f"Deadline: {issue.deadline}")
    print(f"Priority: {issue.priority}")

    print("\nVALIDATED TYPE")
    print("--------------")
    print(type(issue).__name__)


if __name__ == "__main__":
    main()