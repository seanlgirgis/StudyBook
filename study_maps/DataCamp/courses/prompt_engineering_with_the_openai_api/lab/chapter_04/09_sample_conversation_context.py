from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content=(
            "You are the customer-service chatbot for ABC Tech Solutions. "
            "Be concise, professional, and friendly. "
            "Answer only from the demonstrated company information."
        ),
    ),

    Message(
        role="user",
        content="Does ABC Tech Solutions build websites?",
    ),
    Message(
        role="assistant",
        content=(
            "Yes. ABC Tech Solutions provides web application development."
        ),
    ),

    Message(
        role="user",
        content="Does the company build mobile apps?",
    ),
    Message(
        role="assistant",
        content=(
            "Yes. ABC Tech Solutions provides mobile application development."
        ),
    ),

    Message(
        role="user",
        content="Can the company build custom software for a business?",
    ),
]

response = ai.get_response(messages=messages)

print(response)