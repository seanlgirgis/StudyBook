from openai_support import OpenAIService


ai = OpenAIService()

incident = """
A dashboard became slow immediately after a deployment.
Database CPU is normal.
Application error rates increased.
Rolling back the deployment restored normal performance.
"""

prompt = f"""
Analyze the incident delimited by triple backticks.

Generate three independent root-cause hypotheses.
For each hypothesis, give one supporting clue.

Then choose the hypothesis best supported by the evidence.

Return exactly this format:

HYPOTHESIS 1: <cause>
EVIDENCE 1: <supporting clue>

HYPOTHESIS 2: <cause>
EVIDENCE 2: <supporting clue>

HYPOTHESIS 3: <cause>
EVIDENCE 3: <supporting clue>

BEST SUPPORTED CAUSE: <selected cause>
WHY: <brief explanation>

```{incident}```
"""

response = ai.get_response(prompt=prompt)

print(response)