from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

from .config import load_config
from .inventory_local import scan_folder


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_reports(batch_path: Path, reports_dir: Path, large_file_threshold_bytes: int) -> Dict[str, Path]:
    files = scan_folder(batch_path)

    inventory_fields = [
        "path",
        "relative_path",
        "parent_folder",
        "filename",
        "extension",
        "size_bytes",
        "created_time",
        "modified_time",
        "guessed_category",
        "is_photo",
        "is_video",
        "is_document",
    ]
    inventory_csv = reports_dir / "file_inventory.csv"
    write_csv(inventory_csv, inventory_fields, files)

    ext_counter = Counter((row["extension"] or "").lower() for row in files)
    ext_rows = [{"extension": k, "file_count": v} for k, v in sorted(ext_counter.items())]
    ext_csv = reports_dir / "extension_summary.csv"
    write_csv(ext_csv, ["extension", "file_count"], ext_rows)

    large_rows = [
        {"relative_path": row["relative_path"], "size_bytes": row["size_bytes"]}
        for row in files
        if int(row["size_bytes"]) >= large_file_threshold_bytes
    ]
    large_rows.sort(key=lambda r: (-int(r["size_bytes"]), str(r["relative_path"])))
    large_csv = reports_dir / "large_files.csv"
    write_csv(large_csv, ["relative_path", "size_bytes"], large_rows)

    folder_sizes = defaultdict(int)
    for row in files:
        parent = Path(str(row["relative_path"]))
        folder_key = str(parent.parent)
        folder_sizes[folder_key] += int(row["size_bytes"])
    folder_rows = [{"folder": k, "total_size_bytes": v} for k, v in sorted(folder_sizes.items())]
    folder_csv = reports_dir / "folder_sizes.csv"
    write_csv(folder_csv, ["folder", "total_size_bytes"], folder_rows)

    by_name = defaultdict(list)
    for row in files:
        by_name[str(row["filename"]).lower()].append(row)
    same_name_rows: List[Dict[str, object]] = []
    for key, rows in sorted(by_name.items()):
        if len(rows) > 1:
            for row in sorted(rows, key=lambda r: str(r["relative_path"])):
                same_name_rows.append(
                    {
                        "filename_key": key,
                        "filename": row["filename"],
                        "relative_path": row["relative_path"],
                        "size_bytes": row["size_bytes"],
                    }
                )
    same_name_csv = reports_dir / "same_filename_candidates.csv"
    write_csv(same_name_csv, ["filename_key", "filename", "relative_path", "size_bytes"], same_name_rows)

    return {
        "file_inventory": inventory_csv,
        "extension_summary": ext_csv,
        "large_files": large_csv,
        "folder_sizes": folder_csv,
        "same_filename_candidates": same_name_csv,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build CSV reports for a hydrated batch")
    parser.add_argument("--batch-name", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config()
    batch_path = cfg.lab_path("hydrated_dir") / args.batch_name
    reports_dir = cfg.lab_path("reports_dir") / args.batch_name

    if not batch_path.exists():
        raise FileNotFoundError(f"Batch folder not found: {batch_path}")

    outputs = build_reports(batch_path, reports_dir, cfg.large_file_threshold_bytes)
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
