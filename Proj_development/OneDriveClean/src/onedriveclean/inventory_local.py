from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .config import load_config

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".webp", ".raw"}
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".3gp", ".webm"}
DOCUMENT_EXT = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"}
SPREADSHEET_EXT = {".xls", ".xlsx", ".csv", ".tsv"}
PRESENTATION_EXT = {".ppt", ".pptx", ".key"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz"}
CODE_EXT = {".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".sh", ".ps1"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"}


def guess_category(extension: str) -> str:
    ext = extension.lower()
    if ext in PHOTO_EXT:
        return "photo"
    if ext in VIDEO_EXT:
        return "video"
    if ext in DOCUMENT_EXT:
        return "document"
    if ext in SPREADSHEET_EXT:
        return "spreadsheet"
    if ext in PRESENTATION_EXT:
        return "presentation"
    if ext in ARCHIVE_EXT:
        return "archive"
    if ext in CODE_EXT:
        return "code"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def _to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts).isoformat(timespec="seconds")


def scan_folder(folder: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        stat = path.stat()
        ext = path.suffix.lower()
        category = guess_category(ext)
        rel = path.relative_to(folder)
        rows.append(
            {
                "path": str(path),
                "relative_path": str(rel),
                "parent_folder": str(path.parent),
                "filename": path.name,
                "extension": ext,
                "size_bytes": int(stat.st_size),
                "created_time": _to_iso(stat.st_ctime),
                "modified_time": _to_iso(stat.st_mtime),
                "guessed_category": category,
                "is_photo": category == "photo",
                "is_video": category == "video",
                "is_document": category == "document",
            }
        )
    return rows


def resolve_batch_paths(batch_name: str) -> tuple[Path, Path]:
    cfg = load_config()
    batch_path = cfg.lab_path("hydrated_dir") / batch_name
    reports_path = cfg.lab_path("reports_dir") / batch_name
    return batch_path, reports_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan a local hydrated batch folder.")
    parser.add_argument("--batch-name", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_path, _ = resolve_batch_paths(args.batch_name)
    if not batch_path.exists():
        raise FileNotFoundError(f"Batch folder not found: {batch_path}")
    rows = scan_folder(batch_path)
    print(f"Scanned {len(rows)} files from {batch_path}")


if __name__ == "__main__":
    main()
