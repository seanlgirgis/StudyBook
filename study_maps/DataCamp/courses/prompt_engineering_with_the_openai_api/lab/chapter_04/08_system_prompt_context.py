from openai_support import Message, OpenAIService


ai = OpenAIService()

company_context = """
ABC Tech Solutions provides exactly three services:
1. Web application development
2. Mobile application development
3. Custom software solutions
"""

messages = [
    Message(
        role="system",
        content=f"""
You are the customer-service chatbot for ABC Tech Solutions.

Use only the company context below when answering questions about services.
Be concise, professional, and friendly.

If the answer is not contained in the context, reply exactly:
"I do not have that information. Please contact a company representative."

COMPANY CONTEXT:
```{company_context}```
""",
    ),
    Message(
        role="user",
        content="How many services does the company offer, and what are they?",
    ),
]

response = ai.get_response(messages=messages)

print(response)