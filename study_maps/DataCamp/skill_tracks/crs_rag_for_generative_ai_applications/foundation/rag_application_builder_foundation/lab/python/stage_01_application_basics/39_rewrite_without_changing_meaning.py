"""Stage 1, Brick 39: Rewrite text without changing its meaning.

Functionality studied:
    Transform a technical message into clearer customer-facing language
    while preserving required facts.

Reusable mechanics:
    TextGenerationRequest, OpenAITextProvider, and TextGenerationResult
    are provided by rag_foundation.

No new shared abstraction is needed for this brick.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


SOURCE_TEXT = """
Authentication failed because the password-reset token exceeded its
fifteen-minute validity window. Generate a new token and complete the
reset before the replacement token expires.
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=(
            "Rewrite the supplied text for a nontechnical customer. "
            "Use plain English and exactly two short sentences. "
            "Preserve these facts: the reset link expired after fifteen "
            "minutes, the customer must request a new link, and the new "
            "link must be used before it expires. "
            "Do not add advice, apologies, or facts not present in the source."
        ),
        prompt=SOURCE_TEXT,
        model="gpt-5.4-nano",
    )

    result = provider.generate(request)

    print("SOURCE TEXT")
    print("-----------")
    print(SOURCE_TEXT)

    print("\nREWRITTEN TEXT")
    print("--------------")
    print(result.require_text())


if __name__ == "__main__":
    main()
