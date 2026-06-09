from openai_support import OpenAIService


ai = OpenAIService()

message = """
Your support ticket is still open because our team has not finished reviewing it.
We will contact you when we have more information.
"""

prompt = f"""
Rewrite the message delimited by triple backticks.

Requirements:
- Use a professional and empathetic customer-service tone.
- Preserve the original facts.
- Do not promise a resolution date.
- Keep the response under 80 words.

```{message}```
"""

response = ai.get_response(prompt=prompt)

print(response)