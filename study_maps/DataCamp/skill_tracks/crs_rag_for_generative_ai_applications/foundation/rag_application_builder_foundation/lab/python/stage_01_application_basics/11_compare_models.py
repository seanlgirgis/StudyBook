"""Stage 1, Tiny Block 11: Compare two models.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Send the same prompt and instructions to two different models,
    then compare their normalized results.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = "Explain semantic search in one short sentence."

INSTRUCTIONS = """
Use plain English.
Do not use unexplained technical terms.
""".strip()

MODEL_A = "gpt-5.4-mini"
MODEL_B = "gpt-5.4-nano"


def generate_with_model(
    provider: OpenAITextProvider,
    model_name: str,
):
    """Send the shared prompt through one selected model."""

    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=INSTRUCTIONS,
        model=model_name,
    )

    return provider.generate(request)


def main() -> None:
    provider = OpenAITextProvider()

    result_a = generate_with_model(
        provider,
        MODEL_A,
    )

    result_b = generate_with_model(
        provider,
        MODEL_B,
    )

    print("MODEL A")
    print("-------")
    print(result_a.model)
    print(result_a.text)
    print(f"Total tokens: {result_a.total_tokens}")

    print("\nMODEL B")
    print("-------")
    print(result_b.model)
    print(result_b.text)
    print(f"Total tokens: {result_b.total_tokens}")


if __name__ == "__main__":
    main()