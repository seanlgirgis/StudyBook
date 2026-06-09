from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content=(
            "You are a helpful technology support chatbot. "
            "Explain technical issues in simple language. "
            "Keep answers under four sentences."
        ),
    ),
    Message(
        role="user",
        content="Why is my computer running slowly?",
    ),
]

response = ai.get_response(messages=messages)

print(response)