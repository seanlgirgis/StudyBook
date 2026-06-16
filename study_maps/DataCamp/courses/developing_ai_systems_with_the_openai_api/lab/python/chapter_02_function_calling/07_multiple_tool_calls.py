import json

from openai import OpenAI


client = OpenAI()


def get_current_weather(location: str) -> str:
    return f"Demo weather for {location}: sunny and 28°C."


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> str:
    demo_rate = 0.02
    converted_amount = amount * demo_rate

    return (
        f"{amount:.2f} {from_currency} is approximately "
        f"{converted_amount:.2f} {to_currency}."
    )


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
            "role": "user",
            "content": (
                "Tell me the weather in Cairo and convert "
                "100 US dollars to Egyptian pounds."
            ),
        }
    ],
    tools=[weather_tool, currency_tool],
    tool_choice="auto",
)


message = response.choices[0].message

if not message.tool_calls:
    raise ValueError("The model did not select any tools.")


results = []

for tool_call in message.tool_calls:
    arguments = json.loads(tool_call.function.arguments)
    function_name = tool_call.function.name

    if function_name == "get_current_weather":
        location = str(
            arguments.get("location", "")
        ).strip()

        if not location:
            raise ValueError("A location is required.")

        result = get_current_weather(location)

    elif function_name == "convert_currency":
        amount = float(arguments["amount"])
        from_currency = str(
            arguments["from_currency"]
        ).upper()
        to_currency = str(
            arguments["to_currency"]
        ).upper()

        result = convert_currency(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
        )

    else:
        raise ValueError(
            f"Unexpected tool requested: {function_name}"
        )

    results.append(
        {
            "tool": function_name,
            "arguments": arguments,
            "result": result,
        }
    )


print(f"Number of tool calls: {len(results)}")
print("=" * 50)

for item in results:
    print(f"Tool: {item['tool']}")
    print(f"Arguments: {item['arguments']}")
    print(f"Result: {item['result']}")
    print("-" * 50)

print(
    "Important: both local functions use simulated "
    "teaching data."
)
