from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content=(
            "Solve each problem using a brief calculation, "
            "then provide the final answer."
        ),
    ),
    Message(
        role="user",
        content="A team handles 60 tickets in 3 hours. How many per hour?",
    ),
    Message(
        role="assistant",
        content="60 ÷ 3 = 20. Final answer: 20 tickets per hour.",
    ),
    Message(
        role="user",
        content="A team handles 150 tickets in 5 hours. How many per hour?",
    ),
]

response = ai.get_response(messages=messages)

print(response)