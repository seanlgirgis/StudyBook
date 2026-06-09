from __future__ import annotations

import time
from openai import OpenAI


def send_message(
    client: OpenAI,
    messages: list[dict[str, str]],
    user_text: str,
    pause_seconds: int = 3,
) -> str:
    """Append a user message, call the API, save the assistant reply, and return it."""
    print("="*125)
    messages.append({
        "role": "user",
        "content": user_text,
    })

    print(f"\nYou: {user_text}")
    print(f"Waiting {pause_seconds} seconds before the API call...")
    time.sleep(pause_seconds)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        max_completion_tokens=150,
        messages=messages,
    )

    reply = response.choices[0].message.content or ""

    messages.append({
        "role": "assistant",
        "content": reply,
    })

    print(f"Assistant: {reply}")
    print(
        f"Tokens — input: {response.usage.prompt_tokens}, "
        f"output: {response.usage.completion_tokens}, "
        f"total: {response.usage.total_tokens}"
    )

    return reply


def main() -> None:
    client = OpenAI()

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a patient Python tutor. "
                "Teach a complete beginner using short explanations."
            ),
        }
    ]

    send_message(client, messages, "What is a Python list?")
    send_message(client, messages, "Give me a tiny example using the same concept.")
    send_message(client, messages, "Now show me how to add one item to that list.")

    print("\n--- Final conversation history ---")
    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message['role']}: {message['content']}")


if __name__ == "__main__":
    main()
