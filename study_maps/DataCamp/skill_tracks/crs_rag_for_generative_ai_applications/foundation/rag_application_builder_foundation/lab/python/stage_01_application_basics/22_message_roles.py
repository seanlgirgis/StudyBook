"""Stage 1, Brick 22: Understand message roles.

Mechanics:
    Handled by rag_foundation.

Functionality studied here:
    Map application instructions, user input, and model output
    to the familiar chat roles.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)


SYSTEM_INSTRUCTIONS = (
    "You are a patient technical tutor. "
    "Use plain English and answer in two short sentences."
)

USER_MESSAGE = "What is a vector embedding?"


def main() -> None:
    provider = OpenAITextProvider()

    request = TextGenerationRequest(
        instructions=SYSTEM_INSTRUCTIONS,
        prompt=USER_MESSAGE,
    )

    result = provider.generate(request)

    assistant_message = result.require_text()

    print("SYSTEM / APPLICATION ROLE")
    print("-------------------------")
    print(request.instructions)

    print("\nUSER ROLE")
    print("---------")
    print(request.prompt)

    print("\nASSISTANT ROLE")
    print("--------------")
    print(assistant_message)


if __name__ == "__main__":
    main()