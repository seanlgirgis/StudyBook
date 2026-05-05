"""Interactive hybrid tester for 04h local orchestrator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src import service

LOG_PATH = Path(__file__).resolve().parent / "outputs" / "hybrid_ask_logs.jsonl"


def _print_sections(sections: list[dict[str, Any]]) -> None:
    if not sections:
        print("Retrieved Sections: (none)")
        return
    print("Retrieved Sections:")
    for section in sections:
        print(
            f"- {section.get('id')} | {section.get('title')} | "
            f"service={section.get('service_type')} | score={section.get('score')}"
        )


def _append_log(record: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    print("=== 04h Hybrid Interactive RAG Tester ===")
    print('Type "exit" to quit.')

    while True:
        query = input("\nEnter customer request: ").strip()
        if query.lower() == "exit":
            print("Exiting 04h hybrid tester.")
            break
        if not query:
            print("Please enter a non-empty request.")
            continue

        try:
            result = service.answer_query(query)
        except Exception as exc:
            print(f"ERROR: service.answer_query failed: {exc}")
            error_record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "original_query": query,
                "cleaned_intent": "",
                "service_type": "unknown",
                "symptoms": [],
                "urgency": "unknown",
                "clarification_needed": False,
                "clarifying_questions": [],
                "retrieved_section_ids": [],
                "final_answer": "",
                "final_provider_used": "error",
                "status": "error",
                "note": f"Runtime error: {exc}",
            }
            _append_log(error_record)
            continue

        print("\n--- Hybrid Result ---")
        print(f"Original Query: {result.get('original_query', '')}")
        print(f"Cleaned Intent: {result.get('cleaned_intent', '')}")
        print(f"Service Type: {result.get('service_type', '')}")
        print(f"Symptoms: {result.get('symptoms', [])}")
        print(f"Urgency: {result.get('urgency', '')}")
        print(f"Clarification Needed: {result.get('clarification_needed', False)}")
        print(f"Clarifying Questions: {result.get('clarifying_questions', [])}")
        _print_sections(result.get("retrieved_sections", []))
        print(f"Final Answer: {result.get('final_answer', '')}")
        print(f"Final Provider Used: {result.get('final_provider_used', '')}")
        print(f"Status: {result.get('status', '')}")
        note = result.get("note", "")
        if note:
            print(f"Note: {note}")

        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "original_query": result.get("original_query", ""),
            "cleaned_intent": result.get("cleaned_intent", ""),
            "service_type": result.get("service_type", ""),
            "symptoms": result.get("symptoms", []),
            "urgency": result.get("urgency", ""),
            "clarification_needed": bool(result.get("clarification_needed", False)),
            "clarifying_questions": result.get("clarifying_questions", []),
            "retrieved_section_ids": [
                section.get("id") for section in result.get("retrieved_sections", [])
            ],
            "final_answer": result.get("final_answer", ""),
            "final_provider_used": result.get("final_provider_used", "none"),
            "status": result.get("status", "error"),
            "note": note,
        }
        _append_log(record)


if __name__ == "__main__":
    main()

