"""Stage 1, Tiny Block 5: Inspect normalized result metadata.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    A model response contains more than generated text.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = """
Explain embeddings in one short sentence.
""".strip()


def main() -> None:
    request = TextGenerationRequest(
        prompt=PROMPT,
    )

    provider = OpenAITextProvider()

    result = provider.generate(request)

    print("GENERATED TEXT")
    print("--------------")
    print(result.text)

    print("\nPROVIDER")
    print("--------")
    print(result.provider)

    print("\nMODEL")
    print("-----")
    print(result.model)

    print("\nREQUEST ID")
    print("----------")
    print(result.request_id)

    print("\nTOKEN USAGE")
    print("-----------")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")
    print(f"Total tokens: {result.total_tokens}")


if __name__ == "__main__":
    main()