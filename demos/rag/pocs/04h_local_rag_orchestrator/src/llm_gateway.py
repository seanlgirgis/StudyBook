"""Local LLM gateway for POC 04h."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


def call_local_llm(
    prompt: str,
    base_url: str = "http://localhost:8002",
    timeout: int = 180,
) -> str:
    endpoint = f"{base_url.rstrip('/')}/infer"
    payload = json.dumps({"query": prompt}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Local LLM call failed: {exc}") from exc

    answer = body.get("answer") if isinstance(body, dict) else None
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Local LLM response missing non-empty 'answer'")

    return answer.strip()