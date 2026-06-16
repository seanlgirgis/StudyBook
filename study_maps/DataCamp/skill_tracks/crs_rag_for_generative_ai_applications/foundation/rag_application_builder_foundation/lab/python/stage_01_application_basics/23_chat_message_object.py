"""Stage 1, Brick 23: Create and inspect one shared ChatMessage.

Reusable mechanics:
    ChatMessage is provided by rag_foundation.

No API request is made in this lesson.
"""

from rag_foundation.models.chat import ChatMessage


def main() -> None:
    message = ChatMessage(
        role="user",
        content="What is a vector embedding?",
    )

    print("CHAT MESSAGE")
    print("------------")
    print(f"Role: {message.role}")
    print(f"Content: {message.content}")
    print(f"Provider form: {message.to_dict()}")


if __name__ == "__main__":
    main()
