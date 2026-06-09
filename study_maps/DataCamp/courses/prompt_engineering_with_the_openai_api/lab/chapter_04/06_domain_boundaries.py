from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content=(
            "You are a financial education chatbot. "
            "Answer only questions about personal finance, banking, saving, "
            "budgeting, credit, and investing. "
            "Use clear language and keep answers under four sentences. "
            "If the request is outside this domain, reply exactly: "
            "'Sorry, I only answer questions about personal finance.'"
        ),
    ),
    Message(
        role="user",
        content="What will the weather be tomorrow?",
    ),
]

response = ai.get_response(messages=messages)

print(response)