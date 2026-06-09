# Working with the OpenAI API — Field Guide

## Course Status

- **Platform:** DataCamp
- **Track:** Developing AI Applications
- **Track position:** Course 1
- **Status:** Completed
- **Canonical slug:** `working_with_the_openai_api`

## Course Big Picture

```text
create client
→ build messages
→ call model
→ inspect response
→ extract assistant text
→ optionally preserve conversation history
```

The API does not automatically remember earlier requests. A multi-turn application stores prior `user` and `assistant` messages and resends the ordered history with each new call.

## Chapter 1 — Introduction to the OpenAI API

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me one productivity tip."}]
)

print(response.choices[0].message.content)
```

Response path:

```text
response → choices → [0] → message → content
```

## Chapter 2 — Prompting OpenAI Models

A useful prompt can include the task, context, tone, format, and constraints.

### F-string prompt

```python
prompt = f"""
Summarize this conversation in one sentence:

{customer_chat}
"""
```

### Temperature

```text
lower temperature → steadier and more repeatable
higher temperature → more varied and creative
```

High temperature can also increase drift and unsupported claims.

### Token usage

```python
print(response.usage.prompt_tokens)
print(response.usage.completion_tokens)
print(response.usage.total_tokens)
```

### Few-shot prompting

Examples teach the expected judgment and output format.

```python
prompt = """
Classify sentiment from 1 to 5.

Love these! = 5
Comfortable, but not very pretty = 2

Shoes fell apart on the second use. =
"""
```

## Chapter 3 — Building Conversations with the OpenAI API

```text
system = behavior, scope, and guardrails
user = the human request
assistant = a model reply or an example answer
```

### Conversation-history pattern

```python
messages.append({"role": "user", "content": user_text})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

reply = response.choices[0].message.content or ""
messages.append({"role": "assistant", "content": reply})
```

### Multi-turn memory

```text
Turn 1: system + user 1
Turn 2: system + user 1 + assistant 1 + user 2
Turn 3: system + user 1 + assistant 1 + user 2 + assistant 2 + user 3
```

Input tokens grow because the conversation history grows.

### Guardrail

```python
{
    "role": "system",
    "content": (
        "You are a Python tutor. "
        "Answer only Python questions. "
        "Politely refuse unrelated topics."
    )
}
```

### Assistant example

```python
messages = [
    {"role": "system", "content": "Give concise country summaries."},
    {"role": "user", "content": "Summarize Portugal."},
    {"role": "assistant", "content": "Portugal borders Spain. Its capital is Lisbon."},
    {"role": "user", "content": "Summarize Greece."}
]
```

## Truncation Protection

```python
choice = response.choices[0]

if choice.finish_reason == "length":
    print("Reply may be truncated.")
```

Do not append a truncated reply to conversation history.

## Local Lab Evidence

The local labs validated basic requests, prompt controls, token usage, few-shot prompting, guardrails, multi-turn history, finish-reason protection, and JSON/text snapshots after each call.

## Common Mistakes

- Hard-coding a real API key.
- Swapping `system` and `user` roles.
- Forgetting that `messages` is a list.
- Assuming the API remembers previous calls.
- Appending a truncated assistant reply.
- Using high temperature for deterministic classification.
- Providing inaccurate few-shot examples.
- Treating tokens as words.

## Quick Memory Map

```text
client = OpenAI()
messages = [...]
response = client.chat.completions.create(...)
reply = response.choices[0].message.content
```

```text
append user → send full history → extract reply → append assistant
```
