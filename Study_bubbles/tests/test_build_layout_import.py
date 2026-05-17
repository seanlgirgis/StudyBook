from __future__ import annotations

import copy
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

from study_bubbles.build_topic import _apply_layout_to_topic, _load_layout


def _topic_copy() -> dict:
    path = PROJECT_ROOT / "topics" / "case_capacity_feature_table.studybubble.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_valid_layout_applies_positions(tmp_path: Path) -> None:
    topic = _topic_copy()
    layout_path = PROJECT_ROOT / "layouts" / "case_capacity_feature_table.layout.json"
    layout, warnings, errors = _load_layout(layout_path, topic.get("id"))
    assert errors == []
    assert warnings == []
    assert layout is not None

    applied, skipped = _apply_layout_to_topic(topic, layout)
    assert applied >= 1
    assert skipped == 0

    feature_table = next(node for node in topic["nodes"] if node["id"] == "feature_table")
    expected = layout["nodes"]["feature_table"]
    assert feature_table["x"] == float(expected["x"])
    assert feature_table["y"] == float(expected["y"])


def test_unknown_layout_node_is_ignored() -> None:
    topic = _topic_copy()
    layout = {
        "topicId": topic["id"],
        "version": 1,
        "nodes": {
            "unknown_node": {"x": 100, "y": 200},
            "feature_table": {"x": 610, "y": 260},
        },
    }
    applied, skipped = _apply_layout_to_topic(topic, layout)
    assert applied == 1
    assert skipped == 0


def test_missing_layout_node_falls_back_without_crash() -> None:
    topic = _topic_copy()
    original = copy.deepcopy(topic)
    layout = {
        "topicId": topic["id"],
        "version": 1,
        "nodes": {
            "feature_table": {"x": 600, "y": 260},
        },
    }
    applied, skipped = _apply_layout_to_topic(topic, layout)
    assert applied == 1
    assert skipped == 0

    untouched = next(node for node in topic["nodes"] if node["id"] == "application_key")
    original_untouched = next(node for node in original["nodes"] if node["id"] == "application_key")
    assert "x" not in untouched and "y" not in untouched
    assert untouched == original_untouched


def test_bad_layout_json_rejected(tmp_path: Path) -> None:
    bad_layout = tmp_path / "bad.layout.json"
    bad_layout.write_text("{not-json", encoding="utf-8")
    layout, warnings, errors = _load_layout(bad_layout, "case_capacity_feature_table")
    assert layout is None
    assert warnings == []
    assert any("invalid layout JSON" in error for error in errors)
