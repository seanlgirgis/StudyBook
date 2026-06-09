from openai_support import OpenAIService


ai = OpenAIService()

notes = """
- Sales increased by 12 percent.
- Support response times slowed.
- Five support engineers will be hired next quarter.
"""

prompt = f"""
Expand the notes delimited by triple backticks into a short business update.

Requirements:
- Write one professional paragraph.
- Keep it under 120 words.
- Preserve every fact.
- Do not invent any additional numbers or causes.

```{notes}```
"""

response = ai.get_response(prompt=prompt)

print(response)