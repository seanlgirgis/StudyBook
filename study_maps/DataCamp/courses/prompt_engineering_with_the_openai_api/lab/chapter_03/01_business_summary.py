from openai_support import OpenAIService


ai = OpenAIService()

report = """
Quarterly sales increased by 12 percent compared with the previous quarter.
The strongest growth came from enterprise customers in North America.
Customer churn fell slightly, but support response times became slower.
Management plans to hire five additional support engineers next quarter.
"""

prompt = f"""
Summarize the business report delimited by triple backticks.

Requirements:
- Use exactly three bullet points.
- Include the strongest positive result.
- Include the main concern.
- Include the planned next action.

```{report}```
"""

response = ai.get_response(prompt=prompt)

print(response)