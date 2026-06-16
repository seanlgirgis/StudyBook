"""Stage 1, Tiny Block 3: Compare vague and precise instructions."""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = "What is retrieval-augmented generation?"

VAGUE_INSTRUCTIONS = """
Explain clearly.
""".strip()

PRECISE_INSTRUCTIONS = """
Explain in plain English.
Use exactly two short sentences.
Do not use unexplained technical terms.
""".strip()


def ask_model(
    provider: OpenAITextProvider,
    instructions: str,
) -> str:
    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=instructions,
    )

    result = provider.generate(request)

    return result.text


def main() -> None:
    provider = OpenAITextProvider()

    vague_result = ask_model(
        provider,
        VAGUE_INSTRUCTIONS,
    )

    precise_result = ask_model(
        provider,
        PRECISE_INSTRUCTIONS,
    )

    print("VAGUE INSTRUCTIONS RESULT")
    print("-------------------------")
    print(vague_result)

    print("\nPRECISE INSTRUCTIONS RESULT")
    print("---------------------------")
    print(precise_result)


if __name__ == "__main__":
    main()