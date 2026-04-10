#!/usr/bin/env python3
"""
Generate one conversion index CSV per topic folder under leetcode/by_topic.

Purpose:
- turn large .md inventories into actionable conversion checklists
- preserve manually edited progress fields on reruns
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BY_TOPIC = ROOT / "leetcode" / "by_topic"
INDEX_NAME = "_conversion_index.csv"

MD_SUFFIX = ".md"
PY_SUFFIX = ".py"

LC_ID_RE = re.compile(r"^(LC\d{1,5})", re.IGNORECASE)
DAY_RE = re.compile(r"^\s*-\s*(Day-\d+)\s*$", re.IGNORECASE)


def to_title_from_stem(stem: str) -> str:
    # LC055_jump-game -> Jump Game
    cleaned = LC_ID_RE.sub("", stem).lstrip("_- ")
    cleaned = cleaned.replace("_", " ").replace("-", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.title() if cleaned else stem


def normalize_lc_id(stem: str) -> str:
    m = LC_ID_RE.match(stem)
    if not m:
        return stem.lower()
    raw = m.group(1).upper()
    digits = re.findall(r"\d+", raw)[0]
    return f"LC{int(digits):03d}"


def parse_seen_in_days(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    days: list[str] = []
    in_section = False

    for line in text:
        if line.strip().lower().startswith("## seen in days"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## "):
            break
        if in_section:
            m = DAY_RE.match(line)
            if m:
                days.append(m.group(1))
    return ";".join(days)


def read_existing_index(index_path: Path) -> dict[str, dict[str, str]]:
    if not index_path.exists():
        return {}

    out: dict[str, dict[str, str]] = {}
    with index_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("source_md", "").strip()
            if key:
                out[key] = row
    return out


def build_rows_for_topic(topic_dir: Path) -> list[dict[str, str]]:
    index_path = topic_dir / INDEX_NAME
    existing = read_existing_index(index_path)

    md_files = sorted([p for p in topic_dir.glob(f"*{MD_SUFFIX}") if p.is_file()])
    rows: list[dict[str, str]] = []
    topic = topic_dir.name

    for md_file in md_files:
        stem = md_file.stem
        lc_id = normalize_lc_id(stem)
        title = to_title_from_stem(stem)
        source_md = md_file.name
        target_py = f"{stem}{PY_SUFFIX}"
        seen_in_days = parse_seen_in_days(md_file)
        py_exists = (topic_dir / target_py).exists()

        previous = existing.get(source_md, {})
        default_status = "done" if py_exists else "todo"

        row = {
            "lc_id": lc_id,
            "title": title,
            "topic": topic,
            "source_md": source_md,
            "target_py": target_py,
            "py_exists": "yes" if py_exists else "no",
            "seen_in_days": seen_in_days,
            "status": previous.get("status", default_status),
            "tags": previous.get("tags", topic),
            "notes": previous.get("notes", ""),
        }
        rows.append(row)

    # Preserve previously captured rows after markdown cleanup.
    # This keeps conversion tracking durable even when source_md files are deleted.
    present_source_md = {r["source_md"] for r in rows}
    for source_md, previous in existing.items():
        if source_md in present_source_md:
            continue
        target_py = previous.get("target_py", "")
        py_exists = (topic_dir / target_py).exists() if target_py else False
        row = {
            "lc_id": previous.get("lc_id", ""),
            "title": previous.get("title", ""),
            "topic": previous.get("topic", topic),
            "source_md": source_md,
            "target_py": target_py,
            "py_exists": "yes" if py_exists else "no",
            "seen_in_days": previous.get("seen_in_days", ""),
            "status": previous.get("status", "todo"),
            "tags": previous.get("tags", topic),
            "notes": previous.get("notes", ""),
        }
        rows.append(row)

    return rows


def write_topic_index(topic_dir: Path, rows: list[dict[str, str]]) -> int:
    index_path = topic_dir / INDEX_NAME
    fieldnames = [
        "lc_id",
        "title",
        "topic",
        "source_md",
        "target_py",
        "py_exists",
        "seen_in_days",
        "status",
        "tags",
        "notes",
    ]

    with index_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> int:
    if not BY_TOPIC.exists():
        raise SystemExit(f"Missing path: {BY_TOPIC}")

    topic_dirs = sorted([p for p in BY_TOPIC.iterdir() if p.is_dir()])
    topic_count = 0
    total_rows = 0

    for topic_dir in topic_dirs:
        rows = build_rows_for_topic(topic_dir)
        # still write an empty index so every topic has one checklist file
        count = write_topic_index(topic_dir, rows)
        topic_count += 1
        total_rows += count

    print(f"Wrote {topic_count} topic index files with {total_rows} total rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
