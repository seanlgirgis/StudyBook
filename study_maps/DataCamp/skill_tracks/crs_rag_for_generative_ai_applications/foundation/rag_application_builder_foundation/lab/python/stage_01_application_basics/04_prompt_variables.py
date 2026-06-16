"""Stage 1, Tiny Block 4: Build a prompt from variables.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Use ordinary Python variables to build a reusable prompt.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


TOPIC = "vector database"
AUDIENCE = "a beginner"
MAX_SENTENCES = 3


PROMPT = f"""
Explain {TOPIC} to {AUDIENCE}.
Use no more than {MAX_SENTENCES} sentences.
""".strip()


def main() -> None:
    request = TextGenerationRequest(
        prompt=PROMPT,
    )

    provider = OpenAITextProvider()

    result = provider.generate(request)

    print("TOPIC")
    print("-----")
    print(TOPIC)

    print("\nAUDIENCE")
    print("--------")
    print(AUDIENCE)

    print("\nFINAL PROMPT")
    print("------------")
    print(request.prompt)

    print("\nMODEL RESULT")
    print("------------")
    print(result.text)


if __name__ == "__main__":
    main()