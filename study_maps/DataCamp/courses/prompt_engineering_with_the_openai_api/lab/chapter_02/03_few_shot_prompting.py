from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content="""You are an expert review sentiment classifier.
Classify each review as Positive, Negative, or Neutral.
Return only the label without any explanation.""",
    ),

    Message(
        role="user",
        content="The service was excellent.",
    ),
    Message(
        role="assistant",
        content="Positive",
    ),

    Message(
        role="user",
        content="The product arrived broken and customer support was unhelpful.",
    ),
    Message(
        role="assistant",
        content="Negative",
    ),

    Message(
        role="user",
        content="The package arrived on time and the product was acceptable.",
    ),
    Message(
        role="assistant",
        content="Neutral",
    ),

    Message(
        role="user",
        content="The item is usable, but nothing about it impressed me.",
    ),
]

response = ai.get_response(messages=messages)

print(response)