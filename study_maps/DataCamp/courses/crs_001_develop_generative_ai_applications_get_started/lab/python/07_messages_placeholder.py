"""Insert prior chat messages into a reusable chat prompt."""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a patient tutor.",
        ),
        MessagesPlaceholder("history"),
        (
            "human",
            "{question}",
        ),
    ]
)

formatted = prompt.invoke(
    {
        "history": [
            HumanMessage(content="What is LCEL?"),
            AIMessage(content="It composes runnable steps."),
        ],
        "question": "Why is it useful?",
    }
)

for message in formatted.messages:
    print(type(message).__name__, ":", message.content)
