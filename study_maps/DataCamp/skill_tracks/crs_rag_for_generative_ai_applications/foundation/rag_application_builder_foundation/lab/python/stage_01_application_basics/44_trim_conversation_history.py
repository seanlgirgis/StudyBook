"""Stage 1, Brick 44: Trim conversation history before the next call.

Functionality studied:
    Compare a full conversation request with a trimmed request.

Reusable mechanics:
    - ChatMessage
    - ConversationRequest
    - OpenAITextProvider
    - keep_recent_messages()

The application decides the history limit.
"""

from rag_foundation.history import keep_recent_messages
from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest
from rag_foundation.providers.openai_text import OpenAITextProvider


MAX_MESSAGES = 4


def main() -> None:
    provider = OpenAITextProvider()

    full_history = [
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
                "A vector embedding represents meaning as numbers "
                "so similar items can be compared."
            ),
        ),
        ChatMessage(
            role="user",
            content="How is it used in RAG?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "RAG compares the query embedding with document "
                "embeddings to retrieve relevant chunks."
            ),
        ),
        ChatMessage(
            role="user",
            content="Why does chunk size matter?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "Chunk size affects whether retrieval returns enough "
                "context without too much unrelated text."
            ),
        ),
        ChatMessage(
            role="user",
            content="Give me one short practical rule.",
        ),
    ]

    full_result = provider.generate_conversation(
        ConversationRequest(
            messages=full_history,
        )
    )

    trimmed_history = keep_recent_messages(
        full_history,
        max_messages=MAX_MESSAGES,
        preserve_system_message=True,
    )

    trimmed_result = provider.generate_conversation(
        ConversationRequest(
            messages=trimmed_history,
        )
    )

    print("FULL HISTORY")
    print("------------")
    print(f"Messages sent: {len(full_history)}")
    print(f"Input tokens: {full_result.input_tokens}")
    print(full_result.require_text())

    print("\nTRIMMED HISTORY")
    print("---------------")
    print(f"Messages sent: {len(trimmed_history)}")
    print(f"Input tokens: {trimmed_result.input_tokens}")
    print(trimmed_result.require_text())

    print("\nMESSAGES KEPT")
    print("-------------")

    for message in trimmed_history:
        print(f"{message.role}: {message.content}")


if __name__ == "__main__":
    main()