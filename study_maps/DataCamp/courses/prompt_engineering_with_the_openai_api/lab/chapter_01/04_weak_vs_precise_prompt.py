from openai_support import Message, OpenAIService


ai = OpenAIService()

system_message = Message(
    role="system",
    content=(
        "You are a university professor. "
        "Use formal technical language, but answer in no more than 4 sentences."
    ),
)

weak_messages = [
    system_message,
    Message(
        role="user",
        content="Tell me about databases.",
    ),
]

precise_messages = [
    system_message,
    Message(
        role="user",
        content=(
            "Explain relational databases to a beginner. "
            "Use a spreadsheet analogy and define tables, rows, columns, "
            "and primary keys in no more than 4 sentences."
        ),
    ),
]

print("WEAK PROMPT\n")
print(ai.get_response(messages=weak_messages))

print("\n" + "=" * 60 + "\n")

print("PRECISE PROMPT\n")
print(ai.get_response(messages=precise_messages))