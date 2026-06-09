from openai_support import Message, OpenAIService


ai = OpenAIService()

conversation_state = """
- The user has a Windows computer.
- The slowdown began after installing a new application.
- Disk space is low.
- A malware scan has not been performed yet.
"""

messages = [
    Message(
        role="system",
        content=(
            "You are a helpful technology support chatbot. "
            "Use the supplied conversation state when answering. "
            "Explain technical issues in simple language. "
            "Keep answers under four sentences."
        ),
    ),
    Message(
        role="user",
        content=f"""
Conversation state:
```{conversation_state}```

Current request:
What should I check first?
""",
    ),
]

response = ai.get_response(messages=messages)

print(response)