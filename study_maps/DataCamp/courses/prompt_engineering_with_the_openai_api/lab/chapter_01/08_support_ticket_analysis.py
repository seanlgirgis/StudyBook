from openai_support import OpenAIService


ai = OpenAIService()

ticket = """
The application crashes whenever a user uploads a large CSV file.
The customer needs help before tomorrow's reporting deadline.
"""

prompt = f"""
Analyze the support ticket delimited by triple backticks.

Determine:
- the main topic
- whether it is urgent
- a short support title

Rules:
- If a deadline is mentioned, set URGENT to Yes.
- Otherwise, set URGENT to No.

Return exactly this format:

TOPIC: <main topic>
URGENT: <Yes or No>
TITLE: <short support title>

```{ticket}```
"""

response = ai.get_response(prompt=prompt)

print(response)