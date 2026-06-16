import json
from typing import Any

import requests
from openai import OpenAI


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

client = OpenAI()


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def geocode_city(location: str) -> dict[str, Any]:
    """Resolve a city name to coordinates using Open-Meteo."""

    response = requests.get(
        GEOCODING_URL,
        params={
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )
    response.raise_for_status()

    results = response.json().get("results") or []

    if not results:
        raise ValueError(
            f"No matching location found for: {location}"
        )

    return results[0]


def get_current_weather(
    location: str,
    temperature_unit: str = "fahrenheit",
) -> dict[str, Any]:
    """Fetch live current weather from Open-Meteo."""

    place = geocode_city(location)

    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "temperature_unit": temperature_unit,
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    current = payload.get("current") or {}
    units = payload.get("current_units") or {}

    weather_code = current.get("weather_code")

    return {
        "location": place.get("name"),
        "country": place.get("country"),
        "latitude": place.get("latitude"),
        "longitude": place.get("longitude"),
        "time": current.get("time"),
        "temperature": current.get("temperature_2m"),
        "temperature_unit": units.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "feels_like_unit": units.get("apparent_temperature"),
        "precipitation": current.get("precipitation"),
        "precipitation_unit": units.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_speed_unit": units.get("wind_speed_10m"),
        "weather_code": weather_code,
        "condition": WEATHER_CODES.get(
            weather_code,
            "Unknown condition",
        ),
    }


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": (
            "Get current live weather for a city "
            "using the Open-Meteo public API."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": (
                        "City name, optionally with country, "
                        "for example Cairo, Egypt."
                    ),
                },
                "temperature_unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": (
                        "Preferred temperature unit."
                    ),
                },
            },
            "required": [
                "location",
                "temperature_unit",
            ],
            "additionalProperties": False,
        },
    },
}


messages: list[dict[str, Any]] = [
    {
        "role": "system",
        "content": (
            "Use the weather tool for current conditions. "
            "Do not guess or invent weather data."
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
    raise ValueError(
        "The model did not request the weather tool."
    )

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

    temperature_unit = str(
        arguments.get("temperature_unit", "")
    ).strip()

    if not location:
        raise ValueError("A location is required.")

    if temperature_unit not in {
        "celsius",
        "fahrenheit",
    }:
        raise ValueError(
            "temperature_unit must be "
            "celsius or fahrenheit"
        )

    weather_data = get_current_weather(
        location=location,
        temperature_unit=temperature_unit,
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

print("Live Open-Meteo data:")
print(json.dumps(weather_data, indent=2))

print("-" * 50)

print("Final assistant response:")
print(final_text)
