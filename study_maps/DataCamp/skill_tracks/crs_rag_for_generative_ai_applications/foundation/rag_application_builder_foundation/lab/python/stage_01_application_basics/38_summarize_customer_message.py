"""Stage 1, Brick 38: Summarize unstructured customer text.

Functionality studied:
    Convert a longer customer message into a short operational summary.

Reusable mechanics:
    Handled by rag_foundation.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


CUSTOMER_MESSAGE = """
I tried to sign in this morning, but my password was rejected.
I requested a password-reset email twice. The first link never arrived,
and the second link had already expired when I opened it. I need access
before an important meeting this afternoon.
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Summarize the customer message in exactly one short sentence. "
            "Include the main problem and the urgency. "
            "Do not add advice or assumptions."
        ),
        prompt=CUSTOMER_MESSAGE,
        model="gpt-5.4-nano",
    )

    result = provider.generate(request)

    print("CUSTOMER MESSAGE")
    print("----------------")
    print(CUSTOMER_MESSAGE)

    print("\nSUMMARY")
    print("-------")
    print(result.require_text())

    print("\nTOKEN USAGE")
    print("-----------")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")


if __name__ == "__main__":
    main()