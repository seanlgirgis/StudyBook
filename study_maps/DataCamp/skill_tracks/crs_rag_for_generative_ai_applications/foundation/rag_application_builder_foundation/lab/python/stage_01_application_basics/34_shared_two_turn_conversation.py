"""Stage 1, Brick 34: Run a real two-turn conversation through rag_foundation.

New behavior proved here:
    The application uses shared ChatMessage, ConversationRequest,
    and OpenAITextProvider conversation support.

No local chat classes or manual history formatting are used.
"""

from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


def main() -> None:
    provider = OpenAITextProvider()

    history = [
        ChatMessage(
            role="system",
            content=(
                "You are a patient technical tutor. "
                "Use plain English and answer briefly."
            ),
        ),
        ChatMessage(
            role="user",
            content="What is a vector embedding?",
        ),
    ]

    first_request = ConversationRequest(
        messages=history,
    )

    first_result = provider.generate_conversation(
        first_request
    )

    history.append(
        ChatMessage(
            role="assistant",
            content=first_result.require_text(),
        )
    )

    history.append(
        ChatMessage(
            role="user",
            content="How is it used in RAG?",
        )
    )

    second_request = ConversationRequest(
        messages=history,
    )

    second_result = provider.generate_conversation(
        second_request
    )

    print("TURN 1 — ASSISTANT")
    print("------------------")
    print(first_result.text)

    print("\nTURN 2 — ASSISTANT")
    print("------------------")
    print(second_result.text)

    print("\nTURN 2 INPUT TOKENS")
    print("-------------------")
    print(second_result.input_tokens)


if __name__ == "__main__":
    main()