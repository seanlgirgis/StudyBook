import json

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "Return valid JSON only. "
                "Use the keys city, country, and attractions. "
                "The attractions value must be a list of three strings."
            ),
        },
        {
            "role": "user",
            "content": "Provide travel information for Cairo.",
        },
    ],
    response_format={"type": "json_object"},
)

raw_content = response.choices[0].message.content

if raw_content is None:
    raise ValueError("The model returned no content.")

travel_data = json.loads(raw_content)

print("Raw JSON text:")
print(raw_content)

print("-" * 50)

print("Parsed Python object:")
print(travel_data)

print("-" * 50)

print("City:")
print(travel_data["city"])
print('-' * 50)
print("\nAttractions:")
for attraction in travel_data["attractions"]:
    print(f"- {attraction}")
print('-' * 50)