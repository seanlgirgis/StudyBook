from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content="You are a helpful event management assistant.",
    ),
    Message(
        role="user",
        content="What are some good conversation starters at networking events?",
    ),
]

response = ai.get_response(messages=messages)

print(response)