from openai_support import Message, OpenAIService


ai = OpenAIService()

user_question = "Explain why a company might move an application to the cloud."

roles = [
    (
        "CUSTOMER SUPPORT AGENT",
        (
            "You are a customer support agent. "
            "Explain the answer in simple, reassuring language. "
            "Keep the response under four sentences."
        ),
    ),
    (
        "PRODUCT MANAGER",
        (
            "You are a product manager. "
            "Focus on customer value, scalability, and product delivery. "
            "Keep the response under four sentences."
        ),
    ),
    (
        "CLOUD ENGINEER",
        (
            "You are a cloud engineer. "
            "Focus on infrastructure, elasticity, reliability, and operations. "
            "Keep the response under four sentences."
        ),
    ),
]

for role_name, system_prompt in roles:
    messages = [
        Message(
            role="system",
            content=system_prompt,
        ),
        Message(
            role="user",
            content=user_question,
        ),
    ]

    response = ai.get_response(messages=messages)

    print(role_name)
    print(response)
    print("\n" + "=" * 60 + "\n")