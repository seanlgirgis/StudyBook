from openai_support import OpenAIService


ai = OpenAIService()

message = """
The customer have reported several issue with the dashboard.
The reports is loading slow and some chart are missing.
"""

prompt = f"""
Proofread the text delimited by triple backticks.

Requirements:
- Correct grammar, spelling, and punctuation.
- Preserve the original meaning.
- Do not add new facts.
- Return only the corrected text.

```{message}```
"""

response = ai.get_response(prompt=prompt)

print(response)