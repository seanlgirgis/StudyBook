import json

from openai import OpenAI


client = OpenAI()


def get_weather(location: str) -> str:
    """Simple local function used to demonstrate tool execution."""
    return f"The weather in {location} is sunny."


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather for a location. Include the temperature, rain conditions, and any other relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location.",
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
)


message = response.choices[0].message

if not message.tool_calls:
    raise ValueError("The model did not return a tool call.")


tool_call = message.tool_calls[0]

if tool_call.function.name != "get_weather":
    raise ValueError(
        f"Unexpected function requested: {tool_call.function.name}"
    )


arguments = json.loads(tool_call.function.arguments)
location = arguments.get("location", "").strip()

if not location:
    raise ValueError("The tool call did not include a valid location.")


result = get_weather(location)

print("Function selected:")
print(tool_call.function.name)

print("-" * 50)

print("Arguments:")
print(arguments)

print("-" * 50)

print("Function result:")
print(result)
