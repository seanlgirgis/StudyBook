import json
from typing import Any

from openai import OpenAI


def validate_travel_data(data: dict[str, Any]) -> None:
    required_keys = {"city", "country", "attractions"}

    missing_keys = required_keys - data.keys()

    if missing_keys:
        raise ValueError(
            f"Missing required keys: {sorted(missing_keys)}"
        )

    if not isinstance(data["city"], str):
        raise TypeError("city must be a string")

    if not isinstance(data["country"], str):
        raise TypeError("country must be a string")

    if not isinstance(data["attractions"], list):
        raise TypeError("attractions must be a list")

    if not all(
        isinstance(item, str)
        for item in data["attractions"]
    ):
        raise TypeError(
            "Every attraction must be a string"
        )


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "Return valid JSON only. "
                "Use the keys city, country, and attractions. "
                "attractions must contain exactly three strings."
            ),
        },
        {
            "role": "user",
            "content": "Provide travel information for Alexandria, Egypt.",
        },
    ],
    response_format={"type": "json_object"},
)

raw_content = response.choices[0].message.content
print("-" * 50)
print("Raw JSON text:")
print(raw_content)

print("-" * 50)


if raw_content is None:
    raise ValueError("The model returned no content.")

travel_data = json.loads(raw_content)

validate_travel_data(travel_data)

print("Validation passed.")
print(f"City: {travel_data['city']}")
print(f"Country: {travel_data['country']}")

print("Attractions:")
for attraction in travel_data["attractions"]:
    print(f"- {attraction}")