from openai import OpenAI

client = OpenAI()

prompt = "Suggest three names for an AI productivity app."

for temperature in [0.2, 1.0]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temperature,
        max_completion_tokens=50,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(f"\nTemperature: {temperature}")
    print(response.choices[0].message.content)
    
    print("Input tokens:", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)