from openai_support import OpenAIService


ai = OpenAIService()

text = """
The customer reports that the dashboard is slow, several charts fail to load,
and the issue started after yesterday's deployment.
"""

prompt = f"""
Analyze the support issue delimited by triple backticks.

Follow these steps:
1. Identify the main problem.
2. Identify the likely trigger.
3. Suggest the first troubleshooting action.

Return exactly this format:

PROBLEM: <main problem>
TRIGGER: <likely trigger>
FIRST ACTION: <first troubleshooting action>

```{text}```
"""

response = ai.get_response(prompt=prompt)

print(response)