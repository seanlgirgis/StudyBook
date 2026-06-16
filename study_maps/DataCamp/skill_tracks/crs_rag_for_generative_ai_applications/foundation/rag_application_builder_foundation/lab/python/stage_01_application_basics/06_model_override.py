"""Stage 1, Tiny Block 6: Override the provider's default model."""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = "Explain semantic search in one short sentence."

OVERRIDE_MODEL = "gpt-5.4-nano"


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        prompt=PROMPT,
        model=OVERRIDE_MODEL,
    )

    result = provider.generate(request)

    print("PROVIDER DEFAULT MODEL")
    print("----------------------")
    print(provider.default_model)

    print("\nREQUEST OVERRIDE MODEL")
    print("----------------------")
    print(request.model)

    print("\nRESULT MODEL")
    print("------------")
    print(result.model)

    print("\nMODEL RESULT")
    print("------------")
    print(result.text)


if __name__ == "__main__":
    main()