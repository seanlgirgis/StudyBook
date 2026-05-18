from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from study_bubbles.build_topic import build_single_file
from study_bubbles.container import load_container_config
from tools.sync_downloaded_layouts import sync_downloaded_layouts


def _build_topic(container, topic_id: str) -> int:
    topic_path = container.topics_dir / f"{topic_id}.studybubble.json"
    if not topic_path.exists():
        print(f"ERROR: topic file not found: {topic_path}")
        return 1

    layout_path: Path | None = None
    candidate = container.layouts_dir / f"{topic_id}.layout.json"
    if candidate.exists():
        layout_path = candidate

    out_html_path = container.outputs_dir / f"{topic_id}.html"
    out_html_path.parent.mkdir(parents=True, exist_ok=True)

    viewer_root = (container.engine_path / "viewer").resolve()
    if not viewer_root.exists():
        print(f"ERROR: viewer folder not found under engine path: {viewer_root}")
        return 1

    return build_single_file(
        topic_path=topic_path,
        out_html_path=out_html_path,
        layout_path=layout_path,
        project_root=container.root,
        viewer_root=viewer_root,
    )


def _topic_ids_from_updated_layouts(updated_files: list[Path]) -> list[str]:
    topic_ids: list[str] = []
    for path in updated_files:
        if path.name.endswith(".layout.json"):
            topic_ids.append(path.name[: -len(".layout.json")])
    return topic_ids


def _run_build(args: argparse.Namespace) -> int:
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    topic_id = (args.topic or container.default_topic or "").strip()
    if not topic_id:
        print("ERROR: No topic id provided. Set [studybubble] default_topic in bubbles.ini or pass a topic id.")
        return 1
    return _build_topic(container, topic_id)


def _run_sync_layout(args: argparse.Namespace) -> int:
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    downloads_dir = Path(args.downloads).resolve() if args.downloads else container.downloads_dir.resolve()
    if not downloads_dir.exists() or not downloads_dir.is_dir():
        print(f"FAIL: downloads_dir does not exist or is not a folder: {downloads_dir}")
        return 1

    report = sync_downloaded_layouts(
        downloads_dir=downloads_dir,
        layouts_dir=container.layouts_dir,
        dry_run=bool(args.dry_run),
    )
    topic_ids = _topic_ids_from_updated_layouts(report.updated_files)

    print(f"downloads_dir: {downloads_dir}")
    print(f"layouts_dir: {container.layouts_dir}")
    print(f"synced_layouts: {len(report.updated_files)}")
    print(f"backups_created: {len(report.backups_created)}")
    print(f"downloads_deleted: {report.deleted_count}")
    print(f"errors: {len(report.errors)}")
    for err in report.errors:
        print(f"WARN: {err}")

    if args.dry_run:
        print("dry_run: true")
        return 0

    exit_code = 0
    rebuilt = 0
    for topic_id in topic_ids:
        rc = _build_topic(container, topic_id)
        if rc == 0:
            rebuilt += 1
        else:
            exit_code = 1
    print(f"rebuilt_topics: {rebuilt}")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="StudyBubble container CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Build topic HTML from current container")
    p_build.add_argument("topic", nargs="?", default=None, help="Optional topic id override")
    p_build.set_defaults(handler=_run_build)

    p_sync = sub.add_parser("sync-layout", help="Sync exported layout files and rebuild updated topics")
    p_sync.add_argument("--downloads", default=None, help="Downloads folder override")
    p_sync.add_argument("--dry-run", action="store_true", help="Plan-only mode; do not copy/delete/rebuild")
    p_sync.set_defaults(handler=_run_sync_layout)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
