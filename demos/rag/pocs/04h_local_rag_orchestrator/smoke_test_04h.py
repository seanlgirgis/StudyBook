"""Smoke test for POC 04h local orchestrator."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import urllib.error
import urllib.request

BASE_URL = "http://localhost:8010"
OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "SMOKE_TEST_RESULT.md"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def write_result(health: dict, ask_result: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 04h Smoke Test Result",
        "",
        f"Run timestamp: {datetime.now().isoformat()}",
        "",
        "## Health",
        "```json",
        json.dumps(health, indent=2),
        "```",
        "",
        "## Ask",
        "```json",
        json.dumps(ask_result, indent=2),
        "```",
        "",
        "PASS: 04h local orchestrator responded successfully.",
    ]
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print("=== 04h Local RAG Orchestrator Smoke Test ===")

    print("\n[1] Health check")
    health = get_json(f"{BASE_URL}/health")
    print(json.dumps(health, indent=2))

    print("\n[2] Ask check")
    ask_result = post_json(
        f"{BASE_URL}/ask",
        {
            "query": "Hi, sorry to bother you. There is water under my sink and I think a pipe is leaking. Can someone help?"
        },
    )
    print(json.dumps(ask_result, indent=2))

    write_result(health, ask_result)
    print(f"\nWrote: {OUTPUT_PATH}")
    print("\nPASS: 04h local orchestrator responded successfully.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        print(f"\nFAIL: Could not reach {BASE_URL}. Is 04h app running on port 8010?")
        print(exc)
        raise SystemExit(1)
    except Exception as exc:
        print("\nFAIL: Smoke test failed.")
        print(exc)
        raise SystemExit(1)