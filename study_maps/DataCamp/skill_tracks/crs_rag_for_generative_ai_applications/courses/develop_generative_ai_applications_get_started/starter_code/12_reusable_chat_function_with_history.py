"""Reuse one chat function while growing conversation history."""

import os

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
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
            "Use prior conversation context when answering. "
            "Answer in no more than two short sentences unless "
            "the user explicitly requests code or a list.",
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


chain = (
    prompt
    | model
    | StrOutputParser()
)


def ask_with_history(
    question: str,
    history: list[BaseMessage],
) -> str:
    """Ask one question and append the complete turn to history."""

    cleaned_question = question.strip()

    if cleaned_question == "":
        raise ValueError(
            "question must not be blank."
        )

    answer = chain.invoke(
        {
            "history": history,
            "question": cleaned_question,
        }
    )

    if not answer.strip():
        raise RuntimeError(
            "The model returned an empty answer."
        )

    history.append(
        HumanMessage(
            content=cleaned_question
        )
    )

    history.append(
        AIMessage(
            content=answer
        )
    )

    return answer


history: list[BaseMessage] = []


questions = [
    "What does LCEL stand for?",
    "Why is it useful?",
    "Show one tiny code pattern.",
]


print("REUSABLE CHAT FUNCTION")
print("----------------------")

for turn_number, question in enumerate(
    questions,
    start=1,
):
    answer = ask_with_history(
        question,
        history,
    )

    print(
        f"\nTURN {turn_number}"
    )
    print(
        "User:",
        question,
    )
    print(
        "Assistant:",
        answer,
    )


print("\nFINAL HISTORY")
print("-------------")

for message in history:
    print(
        f"{type(message).__name__}: "
        f"{message.content}"
    )


expected_message_count = len(questions) * 2

if len(history) != expected_message_count:
    raise RuntimeError(
        "Conversation history has the wrong "
        "number of messages."
    )


print("\nFINAL CHECK")
print("-----------")
print(
    "PASS: one reusable function invoked the chain, "
    "returned each answer, and updated history."
)