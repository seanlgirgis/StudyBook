import json

from openai_support import OpenAIService


ai = OpenAIService()

ticket = """
Customer Maria Lopez reports that invoice INV-4821 shows a duplicate charge
of $249. She requests a refund and says the issue must be resolved before Friday.
"""

prompt = f"""
Analyze the support ticket delimited by triple backticks.

Return valid JSON only with exactly these keys:

{{
  "category": "Billing | Technical | Account | General",
  "customer": "string or null",
  "invoice": "string or null",
  "amount_usd": "number or null",
  "action": "string or null",
  "deadline": "string or null"
}}

```{ticket}```
"""

response = ai.get_response(prompt=prompt)

try:
    data = json.loads(response)

    allowed_categories = {"Billing", "Technical", "Account", "General"}

    if data.get("category") not in allowed_categories:
        raise ValueError("Unexpected category returned.")

    if not isinstance(data.get("amount_usd"), (int, float, type(None))):
        raise TypeError("amount_usd must be numeric or null.")

except (json.JSONDecodeError, ValueError, TypeError) as error:
    print(f"Record rejected: {error}")
else:
    print("Record accepted.")
    print(data)