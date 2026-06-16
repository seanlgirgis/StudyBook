import json
import os
from typing import Any

import requests
from openai import OpenAI


OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

client = OpenAI()


def get_current_weather(
    location: str,
    units: str = "metric",
) -> dict[str, Any]:
    """Fetch current weather from OpenWeather."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set."
        )

    response = requests.get(
        OPENWEATHER_URL,
        params={
            "q": location,
            "appid": api_key,
            "units": units,
        },
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    weather_items = data.get("weather") or []
    weather_description = (
        weather_items[0].get("description", "Unknown")
        if weather_items
        else "Unknown"
    )

    main = data.get("main") or {}
    wind = data.get("wind") or {}

    return {
        "location": data.get("name", location),
        "country": (data.get("sys") or {}).get("country"),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity_percent": main.get("humidity"),
        "condition": weather_description,
        "wind_speed": wind.get("speed"),
        "units": units,
    }


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": (
            "Get the current live weather for a city using OpenWeather."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": (
                        "City and optional country code, "
                        "for example Cairo,EG."
                    ),
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": (
                        "metric returns Celsius; "
                        "imperial returns Fahrenheit."
                    ),
                },
            },
            "required": ["location", "units"],
            "additionalProperties": False,
        },
    },
}


messages: list[dict[str, Any]] = [
    {
        "role": "system",
        "content": (
            "Use the weather tool for current conditions. "
            "Do not guess weather data."
        ),
    },
    {
        "role": "user",
        "content": (
            "What is the weather in Cairo today? "
            "Use Fahrenheit."
        ),
    },
]


first_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[weather_tool],
    tool_choice="auto",
)

assistant_message = first_response.choices[0].message

if not assistant_message.tool_calls:
    raise ValueError("The model did not request the weather tool.")

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

    units = str(
        arguments.get("units", "")
    ).strip()

    if not location:
        raise ValueError("A location is required.")

    if units not in {"metric", "imperial"}:
        raise ValueError(
            "units must be metric or imperial"
        )

    weather_data = get_current_weather(
        location=location,
        units=units,
    )

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(weather_data),
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
        "The model returned no final response."
    )

print("Live weather data:")
print(json.dumps(weather_data, indent=2))

print("-" * 50)

print("Final assistant response:")
print(final_text)
