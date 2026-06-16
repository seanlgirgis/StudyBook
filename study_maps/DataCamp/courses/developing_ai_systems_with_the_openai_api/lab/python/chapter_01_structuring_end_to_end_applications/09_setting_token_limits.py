from openai import OpenAI


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Answer concisely.",
        },
        {
            "role": "user",
            "content": (
                "Explain why token limits matter in an AI application."
            ),
        },
    ],
    max_tokens=40,
)

content = response.choices[0].message.content

if content is None:
    raise ValueError("The model returned no content.")

print("Response:")
print(content)

print("-" * 50)

print("Finish reason:")
print(response.choices[0].finish_reason)

print("-" * 50)

print("Prompt tokens:")
print(response.usage.prompt_tokens)

print("Completion tokens:")
print(response.usage.completion_tokens)

print("Total tokens:")
print(response.usage.total_tokens)