from pathlib import Path

import pytest

from src.kb_loader import load_kb


def test_load_kb_valid() -> None:
    kb_path = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"
    records = load_kb(kb_path)
    assert records
    assert all("id" in r for r in records)


def test_load_kb_missing_required_field(tmp_path: Path) -> None:
    bad = [
        {
            "id": "x",
            "title": "Bad Record",
            "service_type": "plumbing",
            "text": "missing symptoms",
        }
    ]
    target = tmp_path / "bad.json"
    target.write_text(__import__("json").dumps(bad), encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_kb(target)