import json

from openai_support import OpenAIService


ai = OpenAIService()

conversation_state = {
    "confirmed_facts": [
        "The user has a Windows computer",
        "The slowdown began after installing a new application",
        "Disk space is low",
        "A malware scan has not been performed",
    ],
    "recommended_actions": [],
    "completed_actions": [],
    "open_questions": [],
}

current_request = "What should I check first?"

prompt = f"""
You are a technology support chatbot.

Use the current state and the new request.

Return valid JSON only with exactly these keys:

{{
  "answer": "string",
  "updated_state": {{
    "confirmed_facts": ["string"],
    "recommended_actions": ["string"],
    "completed_actions": ["string"],
    "open_questions": ["string"]
  }}
}}

Rules:
- Preserve confirmed facts unless the user corrects them.
- Do not move recommendations into confirmed facts.
- Add newly recommended actions only to recommended_actions.
- Keep the answer under four sentences.
- Do not invent completed actions.
- Do not include Markdown fences.

CURRENT STATE:
```{json.dumps(conversation_state)}```

NEW REQUEST:
```{current_request}```
"""

response = ai.get_response(prompt=prompt)

data = json.loads(response)

print("ANSWER:")
print(data["answer"])

print("\nUPDATED STATE:")
print(json.dumps(data["updated_state"], indent=2))