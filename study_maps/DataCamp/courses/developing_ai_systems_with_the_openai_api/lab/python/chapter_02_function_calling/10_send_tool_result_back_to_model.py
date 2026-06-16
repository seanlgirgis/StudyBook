import json

from openai import OpenAI


client = OpenAI()


def get_current_weather(location: str) -> dict[str, object]:
    """Return simulated weather data for teaching."""
    return {
        "location": location,
        "temperature_c": 28,
        "condition": "Sunny",
        "rain_expected": False,
    }


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


messages = [
    {
        "role": "user",
        "content": "What is the weather in Cairo?",
    }
]


first_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[weather_tool],
    tool_choice="auto",
)


assistant_message = first_response.choices[0].message

if not assistant_message.tool_calls:
    raise ValueError("The model did not request a tool.")


messages.append(assistant_message.model_dump())


for tool_call in assistant_message.tool_calls:
    if tool_call.function.name != "get_current_weather":
        raise ValueError(
            f"Unexpected tool requested: "
            f"{tool_call.function.name}"
        )

    arguments = json.loads(
        tool_call.function.arguments
    )

    location = str(
        arguments.get("location", "")
    ).strip()

    if not location:
        raise ValueError("A location is required.")

    tool_result = get_current_weather(location)

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result),
        }
    )


final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[weather_tool],
)


final_text = (
    final_response
    .choices[0]
    .message
    .content
)

if final_text is None:
    raise ValueError(
        "The model returned no final text response."
    )


print("Local tool result:")
print(json.dumps(tool_result, indent=2))

print("-" * 50)

print("Final model response:")
print(final_text)

print("-" * 50)

print(
    "Important: the first model call selected the tool; "
    "the local function produced the data; "
    "the second model call explained the result."
)
