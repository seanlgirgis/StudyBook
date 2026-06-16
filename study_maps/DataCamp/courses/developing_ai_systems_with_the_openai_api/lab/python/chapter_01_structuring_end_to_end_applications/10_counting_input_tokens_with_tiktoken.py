import tiktoken
from openai import OpenAI

client = OpenAI()

input_message = {
    "role": "user",
    "content": (
        "I'd like to buy a shirt and a jacket. "
        "Can you suggest two color pairings for these items?"
    ),
}

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

num_tokens = len(
    encoding.encode(input_message["content"])
)

print(f"Input tokens: {num_tokens}")

if num_tokens <= 100:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[input_message],
    )

    print(
        response.choices[0].message.content
    )
else:
    print("Message exceeds token limit")