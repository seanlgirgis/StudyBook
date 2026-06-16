import openai
from openai import OpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


client = OpenAI()


@retry(
    retry=retry_if_exception_type(
        (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
        )
    ),
    stop=stop_after_attempt(4),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=8,
    ),
    reraise=True,
)
def get_model_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("The model returned no content.")

    return content


try:
    result = get_model_response(
        "Explain exponential backoff in one sentence."
    )

    print(result)

except (
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.APIConnectionError,
) as exc:
    print("The request failed after all retry attempts.")
    print(type(exc).__name__)
    print(exc)