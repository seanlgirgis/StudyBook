from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {
        "role": "developer",
        "content": "Explain like a patient teacher speaking to a beginner."
    },
    {
        "role": "user",
        "content": "Explain what an API endpoint is in two simple sentences."
    }
],
)

print(response.choices[0].message.content)