"""Stage 1, Brick 45: Summarize older conversation history.

Functionality studied:
    Replace older chat turns with a compact model-generated summary while
    preserving recent messages verbatim.

Reusable mechanics:
    - ChatMessage
    - ConversationRequest
    - OpenAITextProvider
    - build_summarized_history()

The application controls:
    - which messages are considered old;
    - how the summary should be written;
    - how many recent messages remain verbatim;
    - how strongly the final answer must stay grounded in supplied history.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.history import build_summarized_history
from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest


RECENT_MESSAGE_COUNT = 3


def messages_to_text(
    messages: list[ChatMessage],
) -> str:
    """Convert ordered messages into readable text for summarization."""

    lines: list[str] = []

    for message in messages:
        lines.append(
            f"{message.role}: {message.content}"
        )

    return "\n".join(lines)


def main() -> None:
    provider = OpenAITextProvider()

    full_history = [
        ChatMessage(
            role="system",
            content=(
                "You are a patient technical tutor. "
                "Answer using only facts contained in the supplied "
                "conversation history and its summary. "
                "Return exactly one short sentence. "
                "Do not add numbers, recommendations, examples, lists, "
                "or follow-up offers unless they already appear in "
                "the conversation."
            ),
        ),
        ChatMessage(
            role="user",
            content="What is a vector embedding?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "A vector embedding represents meaning as numbers."
            ),
        ),
        ChatMessage(
            role="user",
            content="How is it used in RAG?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "It helps match a query to relevant document chunks."
            ),
        ),
        ChatMessage(
            role="user",
            content="Why does chunk size matter?",
        ),
        ChatMessage(
            role="assistant",
            content=(
                "Chunk size balances focused retrieval with enough context."
            ),
        ),
        ChatMessage(
            role="user",
            content="What practical rule should I remember?",
        ),
    ]

    # Do not summarize the system message or the recent messages.
    non_system_messages = full_history[1:]

    older_messages = non_system_messages[
        :-RECENT_MESSAGE_COUNT
    ]

    summary_request = TextGenerationRequest(
        instructions=(
            "Summarize the earlier conversation in exactly two short "
            "sentences. Preserve only topics and facts explicitly stated "
            "in the supplied conversation. "
            "Do not add examples, numbers, recommendations, assumptions, "
            "or new information. "
            "Do not address the user directly."
        ),
        prompt=messages_to_text(older_messages),
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    summary_result = provider.generate(
        summary_request
    )

    older_summary = summary_result.require_text()

    compact_history = build_summarized_history(
        full_history,
        older_summary=older_summary,
        recent_message_count=RECENT_MESSAGE_COUNT,
        preserve_system_message=True,
    )

    full_result = provider.generate_conversation(
        ConversationRequest(
            messages=full_history,
            temperature=0.0,
        )
    )

    compact_result = provider.generate_conversation(
        ConversationRequest(
            messages=compact_history,
            temperature=0.0,
        )
    )

    print("OLDER-HISTORY SUMMARY")
    print("---------------------")
    print(older_summary)

    print("\nFULL HISTORY RESULT")
    print("-------------------")
    print(f"Messages sent: {len(full_history)}")
    print(f"Input tokens: {full_result.input_tokens}")
    print(full_result.require_text())

    print("\nSUMMARIZED HISTORY RESULT")
    print("-------------------------")
    print(f"Messages sent: {len(compact_history)}")
    print(f"Input tokens: {compact_result.input_tokens}")
    print(compact_result.require_text())

    print("\nTOKEN DIFFERENCE")
    print("----------------")

    if (
        full_result.input_tokens is not None
        and compact_result.input_tokens is not None
    ):
        token_savings = (
            full_result.input_tokens
            - compact_result.input_tokens
        )

        print(f"Input tokens saved: {token_savings}")

    else:
        print("Input-token comparison is unavailable.")

    print("\nCOMPACT HISTORY")
    print("---------------")

    for message in compact_history:
        print(f"{message.role}: {message.content}")


if __name__ == "__main__":
    main()