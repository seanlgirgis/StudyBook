"""Stage 1, Brick 25: Make a real two-turn conversation.

Reusable mechanics:
    ChatMessage, ConversationRequest, and OpenAITextProvider are supplied
    by rag_foundation.

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

    first_result = provider.generate_conversation(
        ConversationRequest(messages=history)
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

    second_result = provider.generate_conversation(
        ConversationRequest(messages=history)
    )

    print("TURN 1 — USER")
    print("-------------")
    print(history[1].content)

    print("\nTURN 1 — ASSISTANT")
    print("------------------")
    print(first_result.text)

    print("\nTURN 2 — USER")
    print("-------------")
    print(history[3].content)

    print("\nTURN 2 — ASSISTANT")
    print("------------------")
    print(second_result.text)


if __name__ == "__main__":
    main()
