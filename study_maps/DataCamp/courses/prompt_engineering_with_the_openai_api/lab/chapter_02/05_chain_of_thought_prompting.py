from openai_support import OpenAIService


ai = OpenAIService()

prompt = """
A support team receives 120 tickets in 6 hours.

Work through the calculation step by step, then give the final answer.

Question:
How many tickets does the team receive per hour?
"""

response = ai.get_response(prompt=prompt)

print(response)