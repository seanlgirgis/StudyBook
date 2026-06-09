from openai_support import OpenAIService


ai = OpenAIService()

message = """
Your invoice has been approved and payment will be processed within five business days.
"""

prompt = f"""
Translate the business message delimited by triple backticks into Spanish.

Requirements:
- Preserve the exact meaning.
- Keep the tone professional.
- Do not add explanations.
- Return only the translated text.

```{message}```
"""

response = ai.get_response(prompt=prompt)

print(response)