from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_FIELDS = [
    "id",
    "title",
    "subtitle",
    "parentTopic",
    "groups",
    "nodes",
    "links",
    "paths",
]

REQUIRED_NODE_FIELDS = ["id", "label", "size", "group", "definition"]
REQUIRED_LINK_FIELDS = ["source", "target", "label"]
REQUIRED_PATH_FIELDS = ["id", "label", "description", "nodeIds"]
VALID_NODE_SIZES = {"core", "support", "detail"}


def _is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def _is_list(value: Any) -> bool:
    return isinstance(value, list)


def load_topic(topic_path: Path) -> dict[str, Any]:
    with topic_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Topic file root must be a JSON object.")
    return data


def validate_topic_data(topic: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    passes: list[str] = []
    errors: list[str] = []

    missing_top = [field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in topic]
    if missing_top:
        errors.append(f"FAIL: missing required top-level fields: {', '.join(missing_top)}")
        return False, passes, errors

    passes.append("PASS: required top-level fields exist")

    if not _is_list(topic["groups"]):
        errors.append("FAIL: groups must be a list")
    if not _is_list(topic["nodes"]):
        errors.append("FAIL: nodes must be a list")
    if not _is_list(topic["links"]):
        errors.append("FAIL: links must be a list")
    if not _is_list(topic["paths"]):
        errors.append("FAIL: paths must be a list")
    if errors:
        return False, passes, errors

    group_names: set[str] = set()
    for idx, group in enumerate(topic["groups"]):
        if not _is_dict(group):
            errors.append(f"FAIL: groups[{idx}] must be an object")
            continue
        if isinstance(group.get("id"), str):
            group_names.add(group["id"])
        if isinstance(group.get("label"), str):
            group_names.add(group["label"])

    node_ids: list[str] = []
    for idx, node in enumerate(topic["nodes"]):
        if not _is_dict(node):
            errors.append(f"FAIL: nodes[{idx}] must be an object")
            continue

        missing_node_fields = [field for field in REQUIRED_NODE_FIELDS if field not in node]
        if missing_node_fields:
            errors.append(
                f"FAIL: nodes[{idx}] missing required fields: {', '.join(missing_node_fields)}"
            )
            continue

        node_id = node["id"]
        node_ids.append(node_id)

        if node.get("size") not in VALID_NODE_SIZES:
            errors.append(
                f"FAIL: node '{node_id}' has invalid size '{node.get('size')}'"
            )

        if node.get("group") not in group_names:
            errors.append(
                f"FAIL: node '{node_id}' group '{node.get('group')}' not found in top-level groups"
            )

        external_links = node.get("externalLinks")
        if external_links is not None:
            if not _is_list(external_links):
                errors.append(f"FAIL: node '{node_id}' externalLinks must be a list")
            else:
                for link_idx, link in enumerate(external_links):
                    if not _is_dict(link):
                        errors.append(
                            f"FAIL: node '{node_id}' externalLinks[{link_idx}] must be an object"
                        )
                        continue
                    if "label" not in link or "href" not in link:
                        errors.append(
                            f"FAIL: node '{node_id}' externalLinks[{link_idx}] must include label and href"
                        )

        child_topics = node.get("childTopics")
        if child_topics is not None:
            if not _is_list(child_topics):
                errors.append(f"FAIL: node '{node_id}' childTopics must be a list")
            else:
                for child_idx, child in enumerate(child_topics):
                    if not _is_dict(child):
                        errors.append(
                            f"FAIL: node '{node_id}' childTopics[{child_idx}] must be an object"
                        )
                        continue
                    if "label" not in child or "topic" not in child:
                        errors.append(
                            f"FAIL: node '{node_id}' childTopics[{child_idx}] must include label and topic"
                        )

        note = node.get("note")
        if note is not None:
            if not _is_dict(note):
                errors.append(f"FAIL: node '{node_id}' note must be an object when present")
            else:
                summary = note.get("summary")
                if summary is not None and not isinstance(summary, str):
                    errors.append(
                        f"FAIL: node '{node_id}' note.summary must be a string when present"
                    )
                image = note.get("image")
                if image is not None:
                    if not _is_dict(image):
                        errors.append(
                            f"FAIL: node '{node_id}' note.image must be an object"
                        )
                    else:
                        if "src" not in image:
                            errors.append(
                                f"FAIL: node '{node_id}' note.image must include src"
                            )
                        elif not isinstance(image.get("src"), str):
                            errors.append(
                                f"FAIL: node '{node_id}' note.image.src must be a string"
                            )
                        if "caption" in image and not isinstance(image.get("caption"), str):
                            errors.append(
                                f"FAIL: node '{node_id}' note.image.caption must be a string when present"
                            )

        if "commonTrap" in node and not isinstance(node.get("commonTrap"), str):
            errors.append(f"FAIL: node '{node_id}' commonTrap must be a string when present")
        if "interviewAnswer" in node and not isinstance(node.get("interviewAnswer"), str):
            errors.append(
                f"FAIL: node '{node_id}' interviewAnswer must be a string when present"
            )
        if "relatedQuestions" in node:
            rq = node.get("relatedQuestions")
            if not _is_list(rq):
                errors.append(
                    f"FAIL: node '{node_id}' relatedQuestions must be a list of strings"
                )
            elif not all(isinstance(x, str) for x in rq):
                errors.append(
                    f"FAIL: node '{node_id}' relatedQuestions must contain only strings"
                )

    if len(node_ids) != len(set(node_ids)):
        errors.append("FAIL: duplicate node ids detected")
    else:
        passes.append("PASS: node ids are unique")

    if not any(err.startswith("FAIL: node '") and "invalid size" in err for err in errors):
        passes.append("PASS: all node sizes are valid")

    if not any("group '" in err and "not found in top-level groups" in err for err in errors):
        passes.append("PASS: all node groups exist")

    node_id_set = set(node_ids)

    for idx, link in enumerate(topic["links"]):
        if not _is_dict(link):
            errors.append(f"FAIL: links[{idx}] must be an object")
            continue
        missing_link_fields = [field for field in REQUIRED_LINK_FIELDS if field not in link]
        if missing_link_fields:
            errors.append(
                f"FAIL: links[{idx}] missing required fields: {', '.join(missing_link_fields)}"
            )
            continue
        if link["source"] not in node_id_set:
            errors.append(
                f"FAIL: links[{idx}] source '{link['source']}' does not exist as node id"
            )
        if link["target"] not in node_id_set:
            errors.append(
                f"FAIL: links[{idx}] target '{link['target']}' does not exist as node id"
            )

    if not any(err.startswith("FAIL: links[") for err in errors):
        passes.append("PASS: all links point to real nodes")

    for idx, path in enumerate(topic["paths"]):
        if not _is_dict(path):
            errors.append(f"FAIL: paths[{idx}] must be an object")
            continue
        missing_path_fields = [field for field in REQUIRED_PATH_FIELDS if field not in path]
        if missing_path_fields:
            errors.append(
                f"FAIL: paths[{idx}] missing required fields: {', '.join(missing_path_fields)}"
            )
            continue

        node_ids_in_path = path.get("nodeIds")
        if not _is_list(node_ids_in_path):
            errors.append(f"FAIL: paths[{idx}].nodeIds must be a list")
            continue

        for path_node_id in node_ids_in_path:
            if path_node_id not in node_id_set:
                errors.append(
                    f"FAIL: paths[{idx}] references unknown node id '{path_node_id}'"
                )

    if not any(err.startswith("FAIL: paths[") for err in errors):
        passes.append("PASS: all study path nodes exist")

    parent_topic = topic.get("parentTopic")
    if parent_topic is not None:
        if not _is_dict(parent_topic):
            errors.append("FAIL: parentTopic must be an object or null")
        elif "label" not in parent_topic or "topic" not in parent_topic:
            errors.append("FAIL: parentTopic must include label and topic")

    optional_field_errors = [
        err
        for err in errors
        if "externalLinks" in err
        or "childTopics" in err
        or "note.image" in err
        or "parentTopic" in err
    ]
    if not optional_field_errors:
        passes.append("PASS: optional link/topic/image fields are structurally valid")

    return len(errors) == 0, passes, errors


def validate_topic_file(topic_path: Path) -> tuple[bool, list[str], list[str]]:
    passes: list[str] = []
    errors: list[str] = []

    try:
        topic = load_topic(topic_path)
    except FileNotFoundError:
        return False, passes, [f"FAIL: topic file not found: {topic_path}"]
    except json.JSONDecodeError as exc:
        return False, passes, [f"FAIL: invalid JSON: {exc}"]
    except ValueError as exc:
        return False, passes, [f"FAIL: {exc}"]

    passes.append("PASS: topic file loaded")

    ok, v_passes, v_errors = validate_topic_data(topic)
    passes.extend(v_passes)
    errors.extend(v_errors)
    return ok, passes, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate StudyBubble topic JSON")
    parser.add_argument("topic_file", help="Path to .studybubble.json topic file")
    args = parser.parse_args(argv)

    ok, passes, errors = validate_topic_file(Path(args.topic_file))

    for line in passes:
        print(line)
    for line in errors:
        print(line)

    if ok:
        print("Topic validation passed.")
        return 0

    print("Topic validation failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
