from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

from study_bubbles.validate_topic import validate_topic_file


@pytest.fixture
def tiny_topic() -> dict:
    topic_path = PROJECT_ROOT / "topics" / "tiny_capacity_demo.studybubble.json"
    return json.loads(topic_path.read_text(encoding="utf-8"))


def _write_topic(tmp_path: Path, topic: dict) -> Path:
    path = tmp_path / "topic.studybubble.json"
    path.write_text(json.dumps(topic, indent=2), encoding="utf-8")
    return path


def test_valid_tiny_topic_passes(tmp_path: Path, tiny_topic: dict) -> None:
    path = _write_topic(tmp_path, copy.deepcopy(tiny_topic))
    ok, _passes, errors = validate_topic_file(path)
    assert ok is True
    assert errors == []


def test_missing_required_top_level_field_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic.pop("title")
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("missing required top-level fields" in e for e in errors)


def test_duplicate_node_id_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][1]["id"] = "telemetry"
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("duplicate node ids detected" in e for e in errors)


def test_invalid_node_size_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["size"] = "giant"
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("invalid size" in e for e in errors)


def test_link_target_missing_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["links"][1]["target"] = "missing_node"
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("target 'missing_node'" in e for e in errors)


def test_path_node_missing_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["paths"][0]["nodeIds"].append("missing_node")
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("references unknown node id 'missing_node'" in e for e in errors)


def test_external_link_missing_href_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["externalLinks"] = [{"label": "Doc"}]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("externalLinks" in e and "label and href" in e for e in errors)


def test_child_topic_missing_topic_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["childTopics"] = [{"label": "Drilldown"}]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("childTopics" in e and "label and topic" in e for e in errors)


def test_parent_topic_shape_with_label_and_topic_passes(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["parentTopic"] = {"label": "Back to Parent", "topic": "parent_topic.studybubble.json"}
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is True
    assert errors == []


def test_child_topics_shape_with_label_and_topic_passes(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["childTopics"] = [
        {"label": "DataFrame", "topic": "dataframe.studybubble.json"}
    ]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is True
    assert errors == []


def test_optional_rehearsal_fields_pass(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["commonTrap"] = "Trap"
    topic["nodes"][0]["interviewAnswer"] = "Answer"
    topic["nodes"][0]["relatedQuestions"] = ["Q1", "Q2"]
    topic["nodes"][0]["note"] = {
        "summary": "Summary",
        "image": {"src": "assets/example.svg", "caption": "Caption"},
    }
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is True
    assert errors == []


def test_related_questions_non_string_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["nodes"][0]["relatedQuestions"] = ["Q1", 42]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("relatedQuestions must contain only strings" in e for e in errors)


def test_map_resources_optional_shape_passes(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["mapResources"] = [
        {"label": "Open Tutorial", "type": "tutorial", "href": "../tutorial/index.html"},
        {"label": "Next Map", "type": "map", "topic": "next_map.studybubble.json"},
    ]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is True
    assert errors == []


def test_map_resources_missing_target_fails(tmp_path: Path, tiny_topic: dict) -> None:
    topic = copy.deepcopy(tiny_topic)
    topic["mapResources"] = [{"label": "Broken Resource"}]
    path = _write_topic(tmp_path, topic)
    ok, _passes, errors = validate_topic_file(path)
    assert ok is False
    assert any("mapResources[0] must include href or topic" in e for e in errors)
