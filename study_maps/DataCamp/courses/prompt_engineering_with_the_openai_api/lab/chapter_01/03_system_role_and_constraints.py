from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content=(
            "You are a university professor. "
            "Use formal technical language, but answer in no more than 3 sentences."
        ),
    ),
    Message(
        role="user",
        content="Explain prompt engineering.",
    ),
]

response = ai.get_response(messages=messages)

print(response)