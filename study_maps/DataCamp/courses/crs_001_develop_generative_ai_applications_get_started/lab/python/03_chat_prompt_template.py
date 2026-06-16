"""Create structured system and human messages."""

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a patient technical tutor. Use plain English.",
        ),
        (
            "human",
            "Explain {topic} in {sentence_count} sentences.",
        ),
    ]
)

messages = prompt.invoke(
    {
        "topic": "LangChain prompt templates",
        "sentence_count": 2,
    }
)

for message in messages.messages:
    print(type(message).__name__)
    print(message.content)
    print()
