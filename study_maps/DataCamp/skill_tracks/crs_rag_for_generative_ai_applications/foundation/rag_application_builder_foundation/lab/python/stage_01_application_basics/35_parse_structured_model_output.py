"""Stage 1, Brick 35: Parse structured model output.

Mechanics:
    JSON parsing and error handling are provided by rag_foundation.

Functionality studied here:
    Ask the model for structured classification data and use the
    parsed fields in application code.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.structured import parse_json_object


CUSTOMER_MESSAGE = (
    "I cannot sign in because my password reset link expired."
)


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Return valid JSON only with exactly these fields: "
            "category, urgency, and summary. "
            "Category must be billing, technical, or general. "
            "Urgency must be low, medium, or high."
        ),
        prompt=CUSTOMER_MESSAGE,
    )

    result = provider.generate(request)

    structured_result = parse_json_object(
        result.require_text()
    )

    print("CATEGORY")
    print("--------")
    print(structured_result["category"])

    print("\nURGENCY")
    print("-------")
    print(structured_result["urgency"])

    print("\nSUMMARY")
    print("-------")
    print(structured_result["summary"])


if __name__ == "__main__":
    main()