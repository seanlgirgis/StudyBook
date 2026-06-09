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

Return valid JSON only with exactly this structure:

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
- Preserve confirmed facts unless corrected by the user.
- Put advice only in recommended_actions.
- Do not invent completed actions.
- Add useful unresolved questions to open_questions.
- Keep the answer under four sentences.
- Do not include Markdown fences.

CURRENT STATE:
```{json.dumps(conversation_state)}```

NEW REQUEST:
```{current_request}```
"""

response = ai.get_response(prompt=prompt)
data = json.loads(response)

expected_top_keys = {"answer", "updated_state"}
expected_state_keys = {
    "confirmed_facts",
    "recommended_actions",
    "completed_actions",
    "open_questions",
}

if set(data) != expected_top_keys:
    raise ValueError("Unexpected top-level keys.")

if set(data["updated_state"]) != expected_state_keys:
    raise ValueError("Unexpected state keys.")

for key in expected_state_keys:
    if not isinstance(data["updated_state"][key], list):
        raise TypeError(f"{key} must be a list.")

if not isinstance(data["answer"], str):
    raise TypeError("answer must be a string.")

print("STATE VALIDATION PASSED")

print("\nANSWER:")
print(data["answer"])

print("\nUPDATED STATE:")
print(json.dumps(data["updated_state"], indent=2))