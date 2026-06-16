"""Stage 1, Tiny Block 13: Constrain and validate classification output."""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


ALLOWED_LABELS = [
    "billing",
    "technical",
    "general",
]

PROMPT = """
Classify this customer question:

How do I reset my password?
""".strip()

INSTRUCTIONS = """
Choose exactly one label:

billing = payments, invoices, charges, or refunds
technical = login, password, software, device, or system problems
general = anything that does not fit the other labels

Return only the label.
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=INSTRUCTIONS,
        model="gpt-5.4-nano",
    )

    result = provider.generate(request)

    predicted_label = result.text.strip().lower()

    print("MODEL OUTPUT")
    print("------------")
    print(predicted_label)

    print("\nVALIDATION")
    print("----------")

    if predicted_label in ALLOWED_LABELS:
        print("Valid label")
    else:
        print("Invalid label")


if __name__ == "__main__":
    main()