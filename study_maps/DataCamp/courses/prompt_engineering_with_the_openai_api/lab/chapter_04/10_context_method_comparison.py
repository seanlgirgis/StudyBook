from openai_support import Message, OpenAIService


ai = OpenAIService()

question = "Can ABC Tech Solutions build custom software for a business?"

system_context_messages = [
    Message(
        role="system",
        content="""
You are the customer-service chatbot for ABC Tech Solutions.

Use only this company context:
- Web application development
- Mobile application development
- Custom software solutions

Be concise, professional, and friendly.
""",
    ),
    Message(
        role="user",
        content=question,
    ),
]

sample_conversation_messages = [
    Message(
        role="system",
        content=(
            "You are the customer-service chatbot for ABC Tech Solutions. "
            "Answer only from the demonstrated company information."
        ),
    ),
    Message(
        role="user",
        content="Does ABC Tech Solutions build websites?",
    ),
    Message(
        role="assistant",
        content="Yes. ABC Tech Solutions provides web application development.",
    ),
    Message(
        role="user",
        content="Does the company build mobile apps?",
    ),
    Message(
        role="assistant",
        content="Yes. ABC Tech Solutions provides mobile application development.",
    ),
    Message(
        role="user",
        content=question,
    ),
]

print("SYSTEM-PROMPT CONTEXT\n")
print(ai.get_response(messages=system_context_messages))

print("\n" + "=" * 60 + "\n")

print("SAMPLE-CONVERSATION CONTEXT\n")
print(ai.get_response(messages=sample_conversation_messages))