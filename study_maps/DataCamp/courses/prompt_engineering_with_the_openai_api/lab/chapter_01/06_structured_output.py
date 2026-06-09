from openai_support import OpenAIService


ai = OpenAIService()

text = """
Artificial intelligence is changing how people work, learn, and create.
It can automate repetitive tasks, support decision-making, and generate new content.
"""

prompt = f"""
Analyze the text delimited by triple backticks.

Return the result using exactly this format:

TOPIC: <main topic>
SUMMARY: <one-sentence summary>

```{text}```
"""

response = ai.get_response(prompt=prompt)

print(response)