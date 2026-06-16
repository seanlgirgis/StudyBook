"""Stage 1, Brick 46: Detect information loss in a chat summary.

Functionality studied:
    A short conversation summary can reduce token usage but may omit facts
    that later questions require.

Reusable mechanics:
    - ChatMessage
    - TextGenerationRequest
    - OpenAITextProvider
    - build_summarized_history()

Application-specific behavior:
    - which facts are important;
    - which later question depends on those facts;
    - how summary completeness is checked.
"""

from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)
from rag_foundation.history import build_summarized_history
from rag_foundation.models.chat import ChatMessage
from rag_foundation.models.requests import ConversationRequest


RECENT_MESSAGE_COUNT = 1


def messages_to_text(
    messages: list[ChatMessage],
) -> str:
    """Convert ordered messages into text for summarization."""

    return "\n".join(
        f"{message.role}: {message.content}"
        for message in messages
    )


def main() -> None:
    provider = OpenAITextProvider()

    full_history = [
        ChatMessage(
            role="system",
            content=(
                "Answer using only information contained in the "
                "conversation history. "
                "If the needed fact is unavailable, say: "
                "'The conversation does not contain that information.' "
                "Answer in one short sentence."
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "For this project, remember that documents are split "
                "into chunks of 400 words with an overlap of 50 words."
            ),
        ),
        ChatMessage(
            role="assistant",
            content=(
                "Understood: chunks are 400 words with a 50-word overlap."
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "We also decided to store the source filename and page "
                "number with every chunk."
            ),
        ),
        ChatMessage(
            role="assistant",
            content=(
                "Understood: each chunk keeps its source filename "
                "and page number."
            ),
        ),
        ChatMessage(
            role="user",
            content="What overlap did we decide to use?",
        ),
    ]

    non_system_messages = full_history[1:]
    older_messages = non_system_messages[:-RECENT_MESSAGE_COUNT]

    # Intentionally request an overly short summary.
    summary_request = TextGenerationRequest(
        instructions=(
            "Summarize the conversation in exactly one short sentence. "
            "Preserve the most important project decision. "
            "Do not add information."
        ),
        prompt=messages_to_text(older_messages),
        model="gpt-5.4-nano",
        temperature=0.0,
    )

    summary_result = provider.generate(summary_request)
    summary = summary_result.require_text()

    compact_history = build_summarized_history(
        full_history,
        older_summary=summary,
        recent_message_count=RECENT_MESSAGE_COUNT,
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

    expected_fact = "50"

    summary_contains_fact = expected_fact in summary

    print("GENERATED SUMMARY")
    print("-----------------")
    print(summary)

    print("\nREQUIRED FACT")
    print("-------------")
    print("Overlap: 50 words")

    print("\nSUMMARY CHECK")
    print("-------------")
    print(
        "Required fact preserved:"
        f" {summary_contains_fact}"
    )

    print("\nFULL HISTORY ANSWER")
    print("-------------------")
    print(full_result.require_text())

    print("\nSUMMARIZED HISTORY ANSWER")
    print("-------------------------")
    print(compact_result.require_text())

    print("\nCONCLUSION")
    print("----------")

    if summary_contains_fact:
        print(
            "The summary preserved the fact needed by the later question."
        )
    else:
        print(
            "The summary lost the fact needed by the later question."
        )


if __name__ == "__main__":
    main()