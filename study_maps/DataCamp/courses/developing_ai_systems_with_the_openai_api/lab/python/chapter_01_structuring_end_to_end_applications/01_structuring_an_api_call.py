from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a concise travel assistant."
        },
        {
            "role": "user",
            "content": "List three attractions in Cairo."
        }
    ]
)

answer = response.choices[0].message.content

print(answer)