"""
Stage 1, Tiny Block 2:
Separate application instructions from the user prompt.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    instructions = how the model should behave
    prompt = what the user is asking
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


INSTRUCTIONS = """
You are a patient technical teacher.
Use plain English.
Answer in no more than two sentences.
""".strip()


PROMPT = """
What is retrieval-augmented generation?
""".strip()


def main() -> None:
    request = TextGenerationRequest(
        prompt=PROMPT,
        instructions=INSTRUCTIONS,
    )

    provider = OpenAITextProvider()

    result = provider.generate(request)

    print("INSTRUCTIONS")
    print("------------")
    print(request.instructions)

    print("\nUSER PROMPT")
    print("-----------")
    print(request.prompt)

    print("\nMODEL RESULT")
    print("------------")
    print(result.text)


if __name__ == "__main__":
    main()