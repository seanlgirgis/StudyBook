"""Stage 1, Brick 33: Compare zero-shot and few-shot prompting.

New behavior proved here:
    The same model receives the same classification task twice.

    Zero-shot:
        The model receives instructions and the new item only.

    Few-shot:
        The model also receives labeled examples before classifying
        the new item.

Mechanics:
    Handled by rag_foundation.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


MODEL = "gpt-5.4-nano"

USER_MESSAGE = "I cannot sign in to my account."


ZERO_SHOT_INSTRUCTIONS = """
Classify the customer message using exactly one label:

billing
technical
general

Return only the label.
""".strip()


FEW_SHOT_INSTRUCTIONS = """
Classify the customer message using exactly one label:

billing
technical
general

Examples:

Message:
I was charged twice for my subscription.
Label:
billing

Message:
My password reset link does not work.
Label:
technical

Message:
What hours is customer service open?
Label:
general

Return only the label.
""".strip()


def classify(
    provider: OpenAITextProvider,
    instructions: str,
) -> str:
    """Classify the shared user message using supplied instructions."""

    request = TextGenerationRequest(
        instructions=instructions,
        prompt=USER_MESSAGE,
        model=MODEL,
    )

    result = provider.generate(request)

    return result.require_text().strip().lower()


def main() -> None:
    provider = OpenAITextProvider()

    zero_shot_result = classify(
        provider=provider,
        instructions=ZERO_SHOT_INSTRUCTIONS,
    )

    few_shot_result = classify(
        provider=provider,
        instructions=FEW_SHOT_INSTRUCTIONS,
    )

    print("USER MESSAGE")
    print("------------")
    print(USER_MESSAGE)

    print("\nZERO-SHOT RESULT")
    print("----------------")
    print(zero_shot_result)

    print("\nFEW-SHOT RESULT")
    print("---------------")
    print(few_shot_result)


if __name__ == "__main__":
    main()