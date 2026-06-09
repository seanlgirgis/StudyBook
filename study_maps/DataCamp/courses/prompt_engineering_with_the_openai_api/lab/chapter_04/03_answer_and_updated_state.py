from openai_support import OpenAIService


ai = OpenAIService()

conversation_state = """
- The user has a Windows computer.
- The slowdown began after installing a new application.
- Disk space is low.
- A malware scan has not been performed yet.
"""

current_request = """
What should I check first?
"""

prompt = f"""
You are a technology support chatbot.

Use the current conversation state and the new request.

Return exactly two sections:

ANSWER:
- Give the user a concise answer in no more than four sentences.

UPDATED STATE:
- Preserve confirmed facts.
- Add only useful new information from the answer.
- Keep the state concise.
- Do not invent facts.
- Use bullet points.

CURRENT STATE:
```{conversation_state}```

NEW REQUEST:
```{current_request}```
"""

response = ai.get_response(prompt=prompt)

print(response)