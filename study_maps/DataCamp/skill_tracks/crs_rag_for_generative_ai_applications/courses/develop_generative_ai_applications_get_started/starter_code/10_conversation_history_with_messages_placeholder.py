"""Use MessagesPlaceholder to continue a real multi-turn conversation."""

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


question = (
    "Why is it useful? "
    "Answer in one short sentence."
)


print("CONVERSATION HISTORY")
print("--------------------")

for message in history:
    print(
        f"{type(message).__name__}: "
        f"{message.content}"
    )


print("\nCURRENT QUESTION")
print("----------------")
print(question)


result = chain.invoke(
    {
        "history": history,
        "question": question,
    }
)


print("\nMODEL ANSWER")
print("------------")
print(result)


print("\nFINAL CHECK")
print("-----------")

if not result.strip():
    raise RuntimeError(
        "The model returned an empty response."
    )

print(
    "PASS: MessagesPlaceholder inserted the prior "
    "conversation before the current question."
)