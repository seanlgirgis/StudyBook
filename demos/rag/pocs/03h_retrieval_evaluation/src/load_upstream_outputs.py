"""Load and validate upstream 03f/03g output artifacts for 03h alignment."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from schemas import UpstreamDecisionOutput, UpstreamRetrievalOutput


def load_03f_retrieval_output(path: Path) -> UpstreamRetrievalOutput:
    """Read and validate the local 03f hybrid retrieval output artifact."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in 03f output file: {path}") from exc

    try:
        return UpstreamRetrievalOutput.model_validate(payload)
    except ValidationError:
        raise


def load_03g_decision_output(path: Path) -> UpstreamDecisionOutput:
    """Read and validate the local 03g retrieval decision output artifact."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in 03g output file: {path}") from exc

    try:
        return UpstreamDecisionOutput.model_validate(payload)
    except ValidationError:
        raise
