"""Stage 1, Brick 27: Inspect token growth in shared conversation history.

Each new request resends the ordered ChatMessage history through
ConversationRequest and OpenAITextProvider.
"""

from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


def print_usage(turn_number: int, result) -> None:
    print(f"TURN {turn_number}")
    print("------")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")
    print(f"Total tokens: {result.total_tokens}")


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

    history.append(
        ChatMessage(
            role="assistant",
            content=second_result.require_text(),
        )
    )
    history.append(
        ChatMessage(
            role="user",
            content="Why does similarity matter?",
        )
    )

    third_result = provider.generate_conversation(
        ConversationRequest(messages=history)
    )

    print_usage(1, first_result)
    print()
    print_usage(2, second_result)
    print()
    print_usage(3, third_result)


if __name__ == "__main__":
    main()
