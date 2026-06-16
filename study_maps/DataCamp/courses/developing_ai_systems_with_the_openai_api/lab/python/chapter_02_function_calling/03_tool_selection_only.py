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
    print("The model did not select a tool.")
else:
    tool_call = message.tool_calls[0]
    arguments = json.loads(
        tool_call.function.arguments
    )

    print("The model selected this function:")
    print(tool_call.function.name)

    print("-" * 50)

    print("The model produced these arguments:")
    print(arguments)

    print("-" * 50)

    print(
        "Important: no weather function was executed "
        "in this script."
    )
