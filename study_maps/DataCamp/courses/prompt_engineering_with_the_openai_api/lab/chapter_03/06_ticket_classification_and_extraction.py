from openai_support import OpenAIService


ai = OpenAIService()

ticket = """
Customer Maria Lopez reports that invoice INV-4821 shows a duplicate charge
of $249. She requests a refund and says the issue must be resolved before Friday.
"""

prompt = f"""
Analyze the support ticket delimited by triple backticks.

Classify the ticket using exactly one category:
Billing, Technical, Account, or General.

Extract these fields:
- customer name
- invoice number
- amount
- requested action
- deadline

Return exactly this format:

CATEGORY: <category>
CUSTOMER: <name>
INVOICE: <invoice number>
AMOUNT: <amount>
ACTION: <requested action>
DEADLINE: <deadline>

Use N/A when a field is not present.

```{ticket}```
"""

response = ai.get_response(prompt=prompt)

print(response)