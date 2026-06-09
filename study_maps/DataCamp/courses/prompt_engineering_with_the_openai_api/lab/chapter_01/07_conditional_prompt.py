from openai_support import OpenAIService


ai = OpenAIService()

text = """
The application crashes when a user uploads a large CSV file.
The customer needs a fix before tomorrow's reporting deadline.
"""

prompt = f"""
Analyze the text delimited by triple backticks.

Rules:
- If the text mentions a deadline, set URGENT to Yes.
- Otherwise, set URGENT to No.
- Generate a short title.

Return exactly this format:

URGENT: <Yes or No>
TITLE: <short title>

```{text}```
"""

response = ai.get_response(prompt=prompt)

print(response)