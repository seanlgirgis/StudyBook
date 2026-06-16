"""Stage 1, Brick 24: Store shared ChatMessage objects in order.

Reusable mechanics:
    ChatMessage is provided by rag_foundation.

No API request is made in this lesson.
"""

from rag_foundation.models.chat import ChatMessage


def main() -> None:
    history = [
        ChatMessage(
            role="system",
            content="You are a patient technical tutor.",
        ),
        ChatMessage(
            role="user",
            content="What is a vector embedding?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "A vector embedding represents meaning as numbers "
                "so similar items can be compared."
            ),
        ),
        ChatMessage(
            role="user",
            content="How is it used in RAG?",
        ),
    ]

    print("CONVERSATION HISTORY")
    print("--------------------")

    for message_number, message in enumerate(history, start=1):
        print(
            f"{message_number}. "
            f"{message.role}: "
            f"{message.content}"
        )


if __name__ == "__main__":
    main()
