"""Manage separate chat histories with RunnableWithMessageHistory."""
"""Demonstrate the deprecated RunnableWithMessageHistory pattern.

This example is retained for learning and comparison.
New stateful applications should prefer LangGraph persistence.
"""
import os

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not available."
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a patient technical tutor. "
            "Use the conversation history when answering. "
            "Answer in no more than two short sentences.",
        ),
        MessagesPlaceholder(
            variable_name="history"
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


model = ChatOpenAI(
    model=os.getenv(
        "OPENAI_MODEL",
        "gpt-5.4-nano",
    ),
)


base_chain = (
    prompt
    | model
    | StrOutputParser()
)


history_store: dict[
    str,
    InMemoryChatMessageHistory,
] = {}


def get_session_history(
    session_id: str,
) -> InMemoryChatMessageHistory:
    """Return the history object for one conversation session."""

    if session_id not in history_store:
        history_store[session_id] = (
            InMemoryChatMessageHistory()
        )

    return history_store[session_id]


chain_with_history = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


def ask(
    session_id: str,
    question: str,
) -> str:
    """Ask one question inside a named conversation session."""

    cleaned_question = question.strip()

    if cleaned_question == "":
        raise ValueError(
            "question must not be blank."
        )

    return chain_with_history.invoke(
        {
            "question": cleaned_question,
        },
        config={
            "configurable": {
                "session_id": session_id,
            }
        },
    )


print("SESSION: sean")
print("-------------")

print(
    ask(
        "sean",
        "What does LCEL stand for?",
    )
)

print(
    ask(
        "sean",
        "Why is it useful?",
    )
)


print("\nSESSION: anna")
print("-------------")

print(
    ask(
        "anna",
        "What is RunnableParallel?",
    )
)

print(
    ask(
        "anna",
        "Give one use case for it.",
    )
)


print("\nSESSION: sean CONTINUES")
print("-----------------------")

print(
    ask(
        "sean",
        "Show me its smallest code pattern.",
    )
)


print("\nHISTORY COUNTS")
print("--------------")

for session_id, history in history_store.items():
    print(
        f"{session_id}: "
        f"{len(history.messages)} messages"
    )


expected_counts = {
    "sean": 6,
    "anna": 4,
}

for session_id, expected_count in expected_counts.items():
    actual_count = len(
        history_store[session_id].messages
    )

    if actual_count != expected_count:
        raise RuntimeError(
            f"{session_id} history contained "
            f"{actual_count} messages; "
            f"expected {expected_count}."
        )


print("\nFINAL CHECK")
print("-----------")
print(
    "PASS: RunnableWithMessageHistory kept separate "
    "histories for two session IDs and updated them "
    "automatically."
)