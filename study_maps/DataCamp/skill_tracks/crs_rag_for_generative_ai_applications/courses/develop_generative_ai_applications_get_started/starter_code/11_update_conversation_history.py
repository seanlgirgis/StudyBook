"""Continue a conversation by appending each new turn to history."""

import os

from langchain_core.messages import AIMessage, HumanMessage
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
            "Use the prior conversation when answering.",
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


history = [
    HumanMessage(
        content="What does LCEL stand for?"
    ),
    AIMessage(
        content=(
            "LCEL stands for LangChain "
            "Expression Language."
        )
    ),
]


questions = [
    "Why is it useful? Answer in one short sentence.",
    "Give me one tiny code pattern that shows it.",
]


for turn_number, question in enumerate(
    questions,
    start=1,
):
    print(
        f"\nTURN {turn_number}"
    )
    print(
        "-" * 20
    )
    print(
        "User:",
        question,
    )

    answer = chain.invoke(
        {
            "history": history,
            "question": question,
        }
    )

    print(
        "Assistant:",
        answer,
    )

    history.append(
        HumanMessage(
            content=question
        )
    )

    history.append(
        AIMessage(
            content=answer
        )
    )


print("\nFINAL HISTORY")
print("-------------")

for message in history:
    print(
        f"{type(message).__name__}: "
        f"{message.content}"
    )


expected_message_count = 2 + (
    len(questions) * 2
)

if len(history) != expected_message_count:
    raise RuntimeError(
        "Conversation history did not contain "
        "the expected number of messages."
    )


print("\nFINAL CHECK")
print("-----------")
print(
    "PASS: every new human question and model answer "
    "was appended to the conversation history."
)