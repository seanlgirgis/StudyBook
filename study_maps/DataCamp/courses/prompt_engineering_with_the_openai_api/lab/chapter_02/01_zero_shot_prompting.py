from openai_support import OpenAIService


ai = OpenAIService()

prompt = """
Classify the sentiment of this review as Positive, Negative, or Neutral.

Review:
The product works exactly as described and arrived earlier than expected.
"""

response = ai.get_response(prompt=prompt)

print(response)