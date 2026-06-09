from openai_support import Message, OpenAIService


ai = OpenAIService()

text = """
A relational database stores information in tables made of rows and columns.
Tables can be connected using keys so related data can be queried together.
"""

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
        content=f"""
Summarize the text between triple backticks in one sentence.

```{text}```
""",
    ),
]

response = ai.get_response(messages=messages)

print(response)