from __future__ import annotations

import argparse
import configparser
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class SyncReport:
    config_path: Path | None = None
    downloads_dir: Path | None = None
    layouts_dir: Path | None = None
    found_count: int = 0
    deleted_count: int = 0
    updated_files: list[Path] = field(default_factory=list)
    backups_created: list[Path] = field(default_factory=list)
    skipped_files: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _load_layout_file(path: Path) -> tuple[dict | None, str | None]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"read failed: {exc}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"invalid json: {exc}"
    if not isinstance(data, dict):
        return None, "json root must be an object"
    topic_id = data.get("topicId")
    nodes = data.get("nodes")
    if not isinstance(topic_id, str) or not topic_id.strip():
        return None, "missing required string topicId"
    if not isinstance(nodes, dict):
        return None, "missing required object nodes"
    return data, None


def sync_downloaded_layouts(
    downloads_dir: Path,
    layouts_dir: Path,
    *,
    dry_run: bool = False,
) -> SyncReport:
    report = SyncReport()
    downloads_dir = downloads_dir.resolve()
    layouts_dir = layouts_dir.resolve()
    report.downloads_dir = downloads_dir
    report.layouts_dir = layouts_dir
    backup_dir = layouts_dir / "backups"

    files = sorted(downloads_dir.glob("*.layout.json"))
    report.found_count = len(files)

    for file_path in files:
        layout, error = _load_layout_file(file_path)
        if error:
            report.skipped_files.append(file_path)
            report.errors.append(f"{file_path.name}: {error}")
            continue

        assert layout is not None
        topic_id = str(layout["topicId"]).strip()
        target_path = layouts_dir / f"{topic_id}.layout.json"
        backup_path: Path | None = None

        try:
            if target_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = backup_dir / f"{topic_id}.layout.{timestamp}.bak.json"
                if not dry_run:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(target_path, backup_path)
                report.backups_created.append(backup_path)

            if not dry_run:
                layouts_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file_path, target_path)
                file_path.unlink()
                report.deleted_count += 1
            report.updated_files.append(target_path)
        except OSError as exc:
            report.skipped_files.append(file_path)
            report.errors.append(f"{file_path.name}: sync failed: {exc}")
            # keep source file in downloads on failure
            continue

    return report


def _print_report(report: SyncReport) -> None:
    print(f"config: {report.config_path if report.config_path else '(default)'}")
    print(f"downloads_dir: {report.downloads_dir}")
    print(f"layouts_dir: {report.layouts_dir}")
    print(f"found: {report.found_count}")
    print(f"updated: {len(report.updated_files)}")
    print(f"backups: {len(report.backups_created)}")
    print(f"deleted: {report.deleted_count}")
    print(f"skipped: {len(report.skipped_files)}")
    print(f"errors: {len(report.errors)}")
    for message in report.errors:
        print(f"WARN: {message}")


def resolve_paths(
    *,
    config_path: Path,
    downloads_override: str | None,
) -> tuple[Path, Path, list[str], Path | None]:
    warnings: list[str] = []
    project_root = Path.cwd().resolve()
    default_downloads = Path.home() / "Downloads"
    downloads_dir = default_downloads
    layouts_dir = project_root / "layouts"
    used_config: Path | None = None

    if config_path.exists():
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        used_config = config_path.resolve()
        if parser.has_section("paths"):
            raw_downloads = parser.get("paths", "downloads_dir", fallback="").strip()
            raw_layouts = parser.get("paths", "layouts_dir", fallback="").strip()
            if raw_downloads:
                downloads_dir = Path(raw_downloads)
            if raw_layouts:
                candidate = Path(raw_layouts)
                layouts_dir = candidate if candidate.is_absolute() else (project_root / candidate)
    else:
        warnings.append(f"WARN: config file not found at {config_path}; using defaults")

    if downloads_override:
        downloads_dir = Path(downloads_override)

    if not downloads_dir.is_absolute():
        downloads_dir = (project_root / downloads_dir).resolve()
    else:
        downloads_dir = downloads_dir.resolve()
    layouts_dir = layouts_dir.resolve()
    return downloads_dir, layouts_dir, warnings, used_config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync downloaded *.layout.json files into project layouts/"
    )
    parser.add_argument(
        "--downloads",
        default=None,
        help="Downloads folder override (wins over config)",
    )
    parser.add_argument(
        "--config",
        default="config/studybubble.ini",
        help="Config path (default: config/studybubble.ini)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without copying/deleting files",
    )
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

    report = sync_downloaded_layouts(downloads_dir=downloads_dir, layouts_dir=layouts_dir, dry_run=bool(args.dry_run))
    report.config_path = used_config if used_config else Path(args.config)
    _print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
