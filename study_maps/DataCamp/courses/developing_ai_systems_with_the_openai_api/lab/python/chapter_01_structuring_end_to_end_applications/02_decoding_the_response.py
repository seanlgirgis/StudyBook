from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain what an API response object is in one sentence.",
        }
    ],
)

print("Full response object:")
print(response)
print('-' * 50)
print("Response Text: ")
print(response.choices[0].message.content)
print('-' * 50)
print("\nModel used:")
print(response.model)
print('-' * 50)
print("\nFinish reason:")
print(response.choices[0].finish_reason)
print('-' * 50)
print("\nAssistant message object:")
print(response.choices[0].message)
print('-' * 50)
print("\nAssistant text:")
print(response.choices[0].message.content)
print('-' * 50)
print("\nToken usage:")
print(response.usage)