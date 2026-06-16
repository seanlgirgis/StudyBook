import json

from openai import OpenAI


client = OpenAI()


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, such as Cairo.",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    },
}


currency_tool = {
    "type": "function",
    "function": {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount to convert.",
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code, such as USD.",
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code, such as EGP.",
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
                "Use convert_currency only when the user provides "
                "an amount, source currency, and target currency. "
                "Do not invent missing values."
            ),
        },
        {
            "role": "user",
            "content": (
                "I am traveling to Cairo and have 100 US dollars."
            ),
        }
    ],
    tools=[
        weather_tool,
        currency_tool,
    ],
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


for tool_call in message.tool_calls:
    arguments = json.loads(
        tool_call.function.arguments
    )

    print("Tool selected:")
    print(tool_call.function.name)

    print("-" * 50)

    print("Arguments:")
    print(arguments)

    print("-" * 50)


print(
    "Important: tool_choice forced the model to use "
    "convert_currency."
)
