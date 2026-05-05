"""Optional Grok gateway for 04h hybrid interactive testing."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


def get_grok_config() -> dict[str, str]:
    api_key = (os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY") or "").strip()
    model = (os.getenv("GROK_MODEL") or "grok-3").strip()
    base_url = (os.getenv("GROK_BASE_URL") or "https://api.x.ai/v1").strip().rstrip("/")
    return {"api_key": api_key, "model": model, "base_url": base_url}


def build_grok_user_prompt(result: dict[str, Any]) -> str:
    sections = result.get("retrieved_sections", [])
    section_lines: list[str] = []
    for idx, section in enumerate(sections, start=1):
        section_lines.append(
            f"[{idx}] id={section.get('id')} title={section.get('title')} "
            f"service_type={section.get('service_type')} score={section.get('score')}\n"
            f"{section.get('text')}"
        )
    section_blob = "\n\n".join(section_lines) if section_lines else "(none)"

    return (
        f"original_query: {result.get('original_query', '')}\n"
        f"cleaned_intent: {result.get('cleaned_intent', '')}\n"
        f"service_type: {result.get('service_type', '')}\n"
        f"symptoms: {result.get('symptoms', [])}\n"
        f"urgency: {result.get('urgency', '')}\n\n"
        f"retrieved_sections:\n{section_blob}\n\n"
        f"local_draft_answer_optional: {result.get('draft_answer', '')}\n\n"
        "Return only the final customer-facing answer."
    )


def call_grok_final_answer(result: dict[str, Any], timeout: int = 90) -> str:
    cfg = get_grok_config()
    if not cfg["api_key"]:
        raise RuntimeError("Grok API key not set")

    endpoint = f"{cfg['base_url']}/chat/completions"
    payload = {
        "model": cfg["model"],
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a customer-facing assistant for North Texas Comfort & Home Services. "
                    "Answer using only the provided knowledge base sections. "
                    "Do not invent safety instructions or service claims. "
                    "Be concise, practical, and friendly. "
                    "If the context is insufficient, ask one clarifying question."
                ),
            },
            {"role": "user", "content": build_grok_user_prompt(result)},
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg['api_key']}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Grok call failed: {exc}") from exc

    try:
        answer = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Grok response missing expected chat completion content") from exc

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Grok response content was empty")
    return answer.strip()
