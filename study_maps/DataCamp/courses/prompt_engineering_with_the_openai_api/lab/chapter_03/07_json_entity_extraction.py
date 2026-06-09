from openai_support import OpenAIService


ai = OpenAIService()

ticket = """
Customer Maria Lopez reports that invoice INV-4821 shows a duplicate charge
of $249. She requests a refund and says the issue must be resolved before Friday.
"""

prompt = f"""
Analyze the support ticket delimited by triple backticks.

Return valid JSON only, using exactly these keys:

{{
  "category": "Billing | Technical | Account | General",
  "customer": "string or null",
  "invoice": "string or null",
  "amount_usd": "number or null",
  "action": "string or null",
  "deadline": "string or null"
}}

Rules:
- Do not include Markdown code fences.
- Use null when a value is missing.
- Do not add extra keys.

```{ticket}```
"""

response = ai.get_response(prompt=prompt)

print(response)