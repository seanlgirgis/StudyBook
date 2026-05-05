import json
from pathlib import Path

import interactive_hybrid_test as hybrid
from src.grok_gateway import build_grok_user_prompt


def test_build_grok_user_prompt_contains_grounding_and_safety_constraints() -> None:
    result = {
        "original_query": "water under sink",
        "cleaned_intent": "sink leak",
        "service_type": "plumbing",
        "symptoms": ["water", "sink", "leak"],
        "urgency": "urgent",
        "draft_answer": "",
        "retrieved_sections": [
            {
                "id": "kb_plumbing_leak_001",
                "title": "Plumbing leak repair",
                "service_type": "plumbing",
                "score": 9,
                "text": "Leak repair details.",
            }
        ],
    }
    prompt = build_grok_user_prompt(result)
    assert "original_query: water under sink" in prompt
    assert "symptoms: ['water', 'sink', 'leak']" in prompt
    assert "id=kb_plumbing_leak_001" in prompt
    assert "Return only the final customer-facing answer." in prompt


def test_append_log_writes_jsonl(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "hybrid_ask_logs.jsonl"
    monkeypatch.setattr(hybrid, "LOG_PATH", target)
    row = {
        "timestamp_utc": "2026-05-05T00:00:00Z",
        "original_query": "q",
        "cleaned_intent": "q",
        "service_type": "unknown",
        "symptoms": [],
        "urgency": "unknown",
        "clarification_needed": False,
        "clarifying_questions": [],
        "retrieved_section_ids": [],
        "final_answer": "",
        "final_provider_used": "unavailable",
        "status": "final_provider_unavailable",
        "note": "n",
    }
    hybrid._append_log(row)
    lines = target.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    loaded = json.loads(lines[0])
    assert loaded["final_provider_used"] == "unavailable"

