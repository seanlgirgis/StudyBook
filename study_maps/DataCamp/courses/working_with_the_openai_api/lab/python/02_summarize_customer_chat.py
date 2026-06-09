from openai import OpenAI

client = OpenAI()

customer_chat = """
Customer: My order arrived damaged.
Agent: I am sorry. I can arrange a replacement.
Customer: Please send it to the same address.
"""

prompt = f"""
Summarize this customer chat in one sentence:

{customer_chat}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)