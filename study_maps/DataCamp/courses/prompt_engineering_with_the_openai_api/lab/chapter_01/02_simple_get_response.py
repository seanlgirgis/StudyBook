from openai_support import OpenAIService


ai = OpenAIService()

prompt = "Explain prompt engineering in one simple sentence."

response = ai.get_response(prompt=prompt)

print(response)