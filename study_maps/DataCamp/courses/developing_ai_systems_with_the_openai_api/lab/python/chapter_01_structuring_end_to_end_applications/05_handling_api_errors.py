import openai
from openai import OpenAI


client = OpenAI()

try:
    response = client.chat.completions.create(
        model="model-that-does-not-exist",
        messages=[
            {
                "role": "user",
                "content": "Explain exception handling in one sentence.",
            }
        ],
    )

    print(response.choices[0].message.content)

except openai.AuthenticationError as exc:
    print("Authentication failed.")
    print(exc)

except openai.RateLimitError as exc:
    print("The request exceeded a rate or quota limit.")
    print(exc)

except openai.APITimeoutError as exc:
    print("The request timed out.")
    print(exc)

except openai.APIConnectionError as exc:
    print("The client could not connect to the API.")
    print(exc)

except openai.NotFoundError as exc:
    print("The requested model or resource was not found.")
    print(f"Status code: {exc.status_code}")
    print(exc)

except openai.APIStatusError as exc:
    print("The API returned another unsuccessful status.")
    print(f"Status code: {exc.status_code}")
    print(exc)

except Exception as exc:
    print("An unexpected application error occurred.")
    print(type(exc).__name__)
    print(exc)