# grok_intent_clarification.py
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Automatically search for .env in current and parent directories
current_path = Path(__file__).resolve()
env_path = None
for parent in [current_path] + list(current_path.parents):
    candidate = parent / ".env"
    if candidate.exists():
        env_path = candidate
        break

if env_path:
    load_dotenv(env_path)
    print(f"[DEBUG] Loaded .env from: {env_path}")
else:
    print("[WARNING] No .env file found in current or parent directories.")

# Read configuration from environment
GROK_API_KEY = os.getenv("XAI_API_KEY")
GROK_MODEL = os.getenv("GROK_LIGHT_MODEL", "grok-3-mini")
DEBUG = os.getenv("GROK_DEBUG", "False").lower() == "true"

if not GROK_API_KEY:
    raise RuntimeError("Missing XAI_API_KEY environment variable")

GROK_ENDPOINT = "https://api.x.ai/v1/chat/completions"

def clarify_intent(user_query: str, max_tokens: int = 80, temperature: float = 0.0) -> str:
    """
    Send a user query to Grok-mini to normalize / clarify intent.
    Returns a normalized query suitable for local retrieval.
    """
    if not user_query.strip():
        if DEBUG:
            print("[DEBUG] Empty query, returning as-is.")
        return user_query

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    # Tuned system + user prompt with strict domain guidance
    payload = {
        "model": GROK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant for the domain of residential AC, heating, plumbing, and home appliances. "
                    "Do NOT consider general English words. Only map user queries to one of these canonical intents: "
                    "AC repair, heating maintenance, plumbing repair, water heater repair, annual maintenance plan. "
                    "Correct typos and paraphrases. Return exactly one of the above intents. If the query is out-of-domain, return 'NO_MATCH'."
                )
            },
            {
                "role": "user",
                "content": f"Normalize this user query: '{user_query}'.\n"
                           "Return ONLY one of the canonical intents above, nothing else.\n"
                           "Examples:\n"
                           "- 'heatng maintaining plan' → 'heating maintenance plan'\n"
                           "- 'plumping issue' → 'plumbing repair'\n"
                           "- 'AC repar service' → 'AC repair'"
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        resp = requests.post(GROK_ENDPOINT, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        clarified = data["choices"][0]["message"]["content"].strip().rstrip(".")
        if DEBUG:
            print(f"[DEBUG] Original query: '{user_query}' → Normalized: '{clarified}'")
        return clarified
    except Exception as e:
        print(f"[Error] Grok call failed: {e}")
        return user_query

# Example usage for testing
if __name__ == "__main__":
    test_queries = ["heatng maintaining plan", "plumping issue", "AC repar service", "car engine repair", ""]
    for q in test_queries:
        print("Original:", q)
        print("Clarified:", clarify_intent(q))
        print("---")