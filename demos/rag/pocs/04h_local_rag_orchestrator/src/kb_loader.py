"""Local knowledge-base loader for POC 04h."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("id", "title", "service_type", "symptoms", "text")


def load_kb(path: str | Path) -> list[dict[str, Any]]:
    kb_path = Path(path)
    if not kb_path.exists():
        raise ValueError(f"KB file not found: {kb_path}")

    try:
        payload = json.loads(kb_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"KB file is not valid JSON: {kb_path}") from exc

    if not isinstance(payload, list):
        raise ValueError("KB must be a JSON array of records")

    validated: list[dict[str, Any]] = []
    for idx, record in enumerate(payload):
        if not isinstance(record, dict):
            raise ValueError(f"KB record at index {idx} must be an object")

        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            raise ValueError(
                f"KB record at index {idx} missing required fields: {', '.join(missing)}"
            )

        if not isinstance(record["symptoms"], list) or not all(
            isinstance(item, str) for item in record["symptoms"]
        ):
            raise ValueError(
                f"KB record at index {idx} has invalid 'symptoms'; expected list[str]"
            )

        for field in ("id", "title", "service_type", "text"):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError(
                    f"KB record at index {idx} has invalid '{field}'; expected non-empty string"
                )

        validated.append(record)

    return validated