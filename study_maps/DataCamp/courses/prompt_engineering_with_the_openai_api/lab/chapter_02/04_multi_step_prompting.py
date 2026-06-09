from openai_support import OpenAIService


ai = OpenAIService()

text = """
The customer reports that the dashboard is slow, several charts fail to load,
and the issue started after yesterday's deployment.
"""

prompt = f"""
Analyze the support issue delimited by triple backticks.

Complete the task in this order:

Step 1: Summarize the main problem in one sentence.
Step 2: Based on Step 1, identify the most likely trigger.
Step 3: Based on Steps 1 and 2, recommend the first troubleshooting action.

Return exactly this format:

STEP 1 - PROBLEM: <summary>
STEP 2 - LIKELY TRIGGER: <trigger>
STEP 3 - FIRST ACTION: <action>

```{text}```
"""

response = ai.get_response(prompt=prompt)

print(response)