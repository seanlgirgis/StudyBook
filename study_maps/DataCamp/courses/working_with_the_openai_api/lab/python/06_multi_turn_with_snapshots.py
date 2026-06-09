from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from openai import OpenAI


SNAPSHOT_DIR = Path("conversation_snapshots")
MAX_COMPLETION_TOKENS = 300


def dump_messages(
    messages: list[dict[str, str]],
    turn_number: int,
    finish_reason: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
) -> None:
    """Write the full stored conversation after each completed API call."""

    SNAPSHOT_DIR.mkdir(exist_ok=True)

    base_name = f"turn_{turn_number:02d}_messages_after_call"

    json_path = SNAPSHOT_DIR / f"{base_name}.json"
    text_path = SNAPSHOT_DIR / f"{base_name}.txt"

    payload = {
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "turn_number": turn_number,
        "finish_reason": finish_reason,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
        "messages": messages,
    }

    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        f"Turn: {turn_number}",
        f"Captured: {payload['captured_at']}",
        f"Finish reason: {finish_reason}",
        (
            "Tokens: "
            f"input={prompt_tokens}, "
            f"output={completion_tokens}, "
            f"total={total_tokens}"
        ),
        "=" * 100,
        "",
    ]

    for index, message in enumerate(messages, start=1):
        lines.append(f"{index}. ROLE: {message['role']}")
        lines.append(message["content"])
        lines.append("")
        lines.append("-" * 100)
        lines.append("")

    text_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Saved snapshot: {text_path}")
    print(f"Saved snapshot: {json_path}")


def send_message(
    client: OpenAI,
    messages: list[dict[str, str]],
    user_text: str,
    turn_number: int,
    pause_seconds: int = 3,
) -> str:
    """Append user input, call the API, validate the reply, save it, and dump history."""

    print("=" * 125)

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
        max_completion_tokens=MAX_COMPLETION_TOKENS,
        messages=messages,
    )

    choice = response.choices[0]
    reply = choice.message.content or ""
    finish_reason = choice.finish_reason or "unknown"

    if not reply.strip():
        raise RuntimeError("The API returned an empty assistant reply.")

    if finish_reason == "length":
        print(
            "WARNING: The reply hit the completion-token ceiling and may be truncated. "
            "It will not be appended to conversation history."
        )

        dump_messages(
            messages=messages,
            turn_number=turn_number,
            finish_reason=finish_reason,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        raise RuntimeError(
            "Conversation stopped because the assistant reply was truncated. "
            "Increase MAX_COMPLETION_TOKENS or request a shorter answer."
        )

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
    print(f"Finish reason: {finish_reason}")

    dump_messages(
        messages=messages,
        turn_number=turn_number,
        finish_reason=finish_reason,
        prompt_tokens=response.usage.prompt_tokens,
        completion_tokens=response.usage.completion_tokens,
        total_tokens=response.usage.total_tokens,
    )

    return reply


def main() -> None:
    client = OpenAI()

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a patient Python tutor. "
                "Teach a complete beginner. "
                "Keep every answer under 80 words and finish every thought completely."
            ),
        }
    ]

    planned_turns = [
        "What is a Python list?",
        "Give me a tiny example using the same concept.",
        "Now show me how to add one item to that list.",
    ]

    for turn_number, user_text in enumerate(planned_turns, start=1):
        send_message(
            client=client,
            messages=messages,
            user_text=user_text,
            turn_number=turn_number,
        )

    print("\n--- Final conversation history ---")
    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message['role']}: {message['content']}")


if __name__ == "__main__":
    main()
