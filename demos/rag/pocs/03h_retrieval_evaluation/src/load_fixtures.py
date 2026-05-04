"""Fixture loader for 03h labeled retrieval evaluation cases."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from schemas import LabeledRetrievalFixture


def load_labeled_retrieval_fixture(path: Path) -> LabeledRetrievalFixture:
    """Read, validate, and return a typed labeled retrieval fixture."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in fixture file: {path}") from exc

    try:
        return LabeledRetrievalFixture.model_validate(payload)
    except ValidationError:
        raise
