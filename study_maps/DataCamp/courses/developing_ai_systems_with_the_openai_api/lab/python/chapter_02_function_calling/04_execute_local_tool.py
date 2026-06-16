import json

from openai import OpenAI


client = OpenAI()


def get_current_weather(location: str) -> str:
    """Local demo function. This does not fetch live weather."""
    return f"Demo weather for {location}: sunny and 28°C."


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


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "What is the weather in Cairo?",
        }
    ],
    tools=[weather_tool],
    tool_choice="auto",
)


message = response.choices[0].message

if not message.tool_calls:
    raise ValueError("The model did not select a tool.")


tool_call = message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)


if tool_call.function.name != "get_current_weather":
    raise ValueError(
        f"Unexpected function requested: {tool_call.function.name}"
    )


location = arguments.get("location", "").strip()

if not location:
    raise ValueError("The tool call did not include a location.")


result = get_current_weather(location)


print("Tool selected by the model:")
print(tool_call.function.name)

print("-" * 50)

print("Arguments created by the model:")
print(arguments)

print("-" * 50)

print("Local function result:")
print(result)
