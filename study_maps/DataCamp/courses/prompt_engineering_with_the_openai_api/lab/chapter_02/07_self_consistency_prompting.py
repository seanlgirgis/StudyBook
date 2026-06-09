from openai_support import OpenAIService


ai = OpenAIService()

prompt = """
Solve the problem in three independent ways.

Problem:
A team processes 240 tickets in 8 hours.
How many tickets does the team process per hour?

Return exactly this format:

METHOD 1: <brief calculation>
METHOD 2: <brief calculation>
METHOD 3: <brief calculation>
FINAL ANSWER: <answer agreed on by the methods>
"""

response = ai.get_response(prompt=prompt)

print(response)