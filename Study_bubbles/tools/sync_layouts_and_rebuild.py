from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.sync_downloaded_layouts import resolve_paths, sync_downloaded_layouts
from study_bubbles.container import load_container_config


@dataclass
class RebuildReport:
    rebuilt_topics: list[str] = field(default_factory=list)
    skipped_topics: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def topic_ids_from_updated_layouts(updated_files: list[Path]) -> list[str]:
    topic_ids: list[str] = []
    for path in updated_files:
        name = path.name
        if name.endswith(".layout.json"):
            topic_ids.append(name[: -len(".layout.json")])
    return topic_ids


def rebuild_topics_for_layouts(topic_ids: list[str], *, dry_run: bool = False) -> RebuildReport:
    report = RebuildReport()
    container = None
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError:
        container = None

    for topic_id in topic_ids:
        if container is not None:
            topic_path = container.topics_dir / f"{topic_id}.studybubble.json"
            layout_path = container.layouts_dir / f"{topic_id}.layout.json"
            out_path = container.outputs_dir / f"{topic_id}.html"
        else:
            topic_path = Path("topics") / f"{topic_id}.studybubble.json"
            layout_path = Path("layouts") / f"{topic_id}.layout.json"
            out_path = Path("outputs") / "single_file" / f"{topic_id}.html"

        if not topic_path.exists():
            report.skipped_topics.append(topic_id)
            report.errors.append(f"WARN: topic source missing for '{topic_id}': {topic_path}")
            continue
        if dry_run:
            report.rebuilt_topics.append(topic_id)
            continue

        if container is not None:
            cmd = [
                sys.executable,
                str(container.engine_path / "tools" / "studybubble.py"),
                "build",
                topic_id,
            ]
        else:
            cmd = [
                sys.executable,
                "-m",
                "src.study_bubbles.build_topic",
                "--topic",
                str(topic_path),
                "--layout",
                str(layout_path),
                "--out",
                str(out_path),
                "--mode",
                "single-file",
            ]
        run = subprocess.run(cmd, capture_output=True, text=True)
        if run.returncode == 0:
            report.rebuilt_topics.append(topic_id)
        else:
            report.errors.append(
                f"FAIL: rebuild failed for '{topic_id}' (exit {run.returncode})\n{run.stdout}\n{run.stderr}".strip()
            )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync exported layouts from Downloads and rebuild matching topics")
    parser.add_argument("--config", default="config/studybubble.ini", help="Config path (default: config/studybubble.ini)")
    parser.add_argument("--downloads", default=None, help="Downloads folder override (wins over config)")
    parser.add_argument("--dry-run", action="store_true", help="Plan-only mode; do not copy/delete/rebuild")
    args = parser.parse_args()

    downloads_dir, layouts_dir, warnings, used_config = resolve_paths(
        config_path=Path(args.config),
        downloads_override=args.downloads,
    )
    for warning in warnings:
        print(warning)
    if not downloads_dir.exists() or not downloads_dir.is_dir():
        print(f"FAIL: downloads_dir does not exist or is not a folder: {downloads_dir}")
        return 1

    sync_report = sync_downloaded_layouts(downloads_dir=downloads_dir, layouts_dir=layouts_dir, dry_run=bool(args.dry_run))
    topic_ids = topic_ids_from_updated_layouts(sync_report.updated_files)
    rebuild_report = rebuild_topics_for_layouts(topic_ids, dry_run=bool(args.dry_run))

    print(f"config: {used_config if used_config else Path(args.config)}")
    print(f"downloads_dir: {downloads_dir}")
    print(f"layouts_dir: {layouts_dir}")
    print(f"synced_layouts: {len(sync_report.updated_files)}")
    print(f"backups_created: {len(sync_report.backups_created)}")
    print(f"downloads_deleted: {sync_report.deleted_count}")
    print(f"rebuilt_topics: {len(rebuild_report.rebuilt_topics)}")
    print(f"skipped_topics: {len(rebuild_report.skipped_topics)}")
    all_errors = list(sync_report.errors) + list(rebuild_report.errors)
    print(f"errors: {len(all_errors)}")
    for err in all_errors:
        print(err)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
