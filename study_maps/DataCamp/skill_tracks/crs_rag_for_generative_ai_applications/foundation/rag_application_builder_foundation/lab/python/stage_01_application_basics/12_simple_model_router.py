"""Stage 1, Tiny Block 12: Route work to a suitable model.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Use a cheaper model for simple work.
    Use a stronger model for work needing more judgment.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


SIMPLE_MODEL = "gpt-5.4-nano"
STRONGER_MODEL = "gpt-5.4-mini"


def choose_model(task_type: str) -> str:
    """Choose a model based on the kind of task."""

    if task_type == "simple":
        return SIMPLE_MODEL

    return STRONGER_MODEL


def run_task(
    provider: OpenAITextProvider,
    task_type: str,
    prompt: str,
):
    """Choose a model, create the request, and return the result."""

    selected_model = choose_model(task_type)

    request = TextGenerationRequest(
        prompt=prompt,
        model=selected_model,
    )

    return provider.generate(request)


def main() -> None:
    provider = OpenAITextProvider()

    simple_result = run_task(
        provider=provider,
        task_type="simple",
        prompt=(
            "Classify this question as billing, technical, or general: "
            "'How do I reset my password?'"
        ),
    )

    complex_result = run_task(
        provider=provider,
        task_type="complex",
        prompt=(
            "Classify this question as billing, technical, or general: "
            "'How do I reset my password?'"
        ),

    )

    print("SIMPLE TASK")
    print("-----------")
    print(f"Model: {simple_result.model}")
    print(simple_result.text)

    print("\nCOMPLEX TASK")
    print("------------")
    print(f"Model: {complex_result.model}")
    print(complex_result.text)


if __name__ == "__main__":
    main()