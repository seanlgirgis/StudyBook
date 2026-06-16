import json

from openai import OpenAI


client = OpenAI()


currency_tool = {
    "type": "function",
    "function": {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": ["number", "null"],
                    "description": "The amount to convert, or null if missing.",
                },
                "from_currency": {
                    "type": ["string", "null"],
                    "description": (
                        "Source currency code, such as USD, "
                        "or null if missing."
                    ),
                },
                "to_currency": {
                    "type": ["string", "null"],
                    "description": (
                        "Target currency code, such as EGP, "
                        "or null if missing."
                    ),
                },
            },
            "required": [
                "amount",
                "from_currency",
                "to_currency",
            ],
            "additionalProperties": False,
        },
    },
}


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "Extract only values explicitly provided by the user. "
                "Use null for missing values. Do not infer currencies "
                "from cities, countries, or travel context."
            ),
        },
        {
            "role": "user",
            "content": (
                "I am traveling to Cairo and have 100 US dollars."
            ),
        },
    ],
    tools=[currency_tool],
    tool_choice={
        "type": "function",
        "function": {
            "name": "convert_currency",
        },
    },
)


message = response.choices[0].message

if not message.tool_calls:
    raise ValueError("The model did not return a tool call.")


tool_call = message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)

amount = arguments.get("amount")
from_currency = arguments.get("from_currency")
to_currency = arguments.get("to_currency")


print("Extracted arguments:")
print(arguments)

print("-" * 50)


missing_fields = []

if amount is None:
    missing_fields.append("amount")

if not from_currency:
    missing_fields.append("from_currency")

if not to_currency:
    missing_fields.append("to_currency")


if missing_fields:
    print("The function will not run.")
    print(f"Missing fields: {missing_fields}")

    if "to_currency" in missing_fields:
        print("Clarifying question:")
        print("Which currency would you like to convert the USD to?")
else:
    print("All required values are present.")
    print("The local conversion function may now run.")
