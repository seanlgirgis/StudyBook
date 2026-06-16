"""Stage 1, Brick 26: Prove that a follow-up needs prior context.

The same follow-up is sent twice:

1. without previous conversation history;
2. with ordered ChatMessage history.

Reusable mechanics are supplied by rag_foundation.
"""

from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


FOLLOW_UP = "How is it used in RAG?"


def main() -> None:
    provider = OpenAITextProvider()

    without_context = ConversationRequest(
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "You are a patient technical tutor. "
                    "Use plain English and answer briefly."
                ),
            ),
            ChatMessage(
                role="user",
                content=FOLLOW_UP,
            ),
        ]
    )

    without_context_result = provider.generate_conversation(
        without_context
    )

    with_context = ConversationRequest(
        messages=[
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
            ChatMessage(
                role="assistant",
                content=(
                    "A vector embedding represents text or other data "
                    "as numbers so similar items can be compared."
                ),
            ),
            ChatMessage(
                role="user",
                content=FOLLOW_UP,
            ),
        ]
    )

    with_context_result = provider.generate_conversation(
        with_context
    )

    print("WITHOUT PREVIOUS CONTEXT")
    print("------------------------")
    print(without_context_result.text)

    print("\nWITH PREVIOUS CONTEXT")
    print("---------------------")
    print(with_context_result.text)


if __name__ == "__main__":
    main()
