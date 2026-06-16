"""Stage 1, Tiny Block 7: Limit the model's maximum output tokens.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Prompt instructions request a certain length.
    max_output_tokens places a technical ceiling on generation.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


PROMPT = """
Explain why vector databases are useful for RAG applications.
""".strip()

INSTRUCTIONS = """
Use plain English.
Give a short explanation.
""".strip()


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=INSTRUCTIONS,
        max_output_tokens=80,
    )

    result = provider.generate(request)

    print("REQUESTED MAXIMUM OUTPUT TOKENS")
    print("-------------------------------")
    print(request.max_output_tokens)

    print("\nMODEL RESULT")
    print("------------")
    print(result.text)

    print("\nACTUAL OUTPUT TOKENS")
    print("--------------------")
    print(result.output_tokens)


if __name__ == "__main__":
    main()