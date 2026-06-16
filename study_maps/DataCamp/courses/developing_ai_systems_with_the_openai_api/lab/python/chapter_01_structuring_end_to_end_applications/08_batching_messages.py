from openai import OpenAI


client = OpenAI()

cities = [
    "Cairo",
    "Alexandria",
    "Luxor",
]


def get_city_summary(city: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise travel assistant. "
                    "Respond in one sentence."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Give a short travel summary for {city}, Egypt."
                ),
            },
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError(
            f"The model returned no content for {city}."
        )

    return content


results: dict[str, str] = {}

for city in cities:
    print(f"Processing {city}...")
    results[city] = get_city_summary(city)


print("\nBatch results")
print("-" * 50)

for city, summary in results.items():
    print(f"{city}:")
    print(summary)
    print("-" * 50)