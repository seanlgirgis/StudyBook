#!/usr/bin/env python3
"""Search coding_challenges/index.csv by substring (grep-like)."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = ROOT / "index.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search coding_challenges/index.csv by substring")
    parser.add_argument("needle", help="Substring to search for (example: 48)")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH, help="Path to .csv index file")
    parser.add_argument("--case-sensitive", action="store_true", help="Use case-sensitive search")
    parser.add_argument("--limit", type=int, default=50, help="Max rows to print")
    return parser.parse_args()


def normalize(text: str, case_sensitive: bool) -> str:
    return text if case_sensitive else text.lower()


def main() -> int:
    args = parse_args()
    index_path = args.index.resolve()

    if not index_path.exists():
        raise SystemExit(f"Index file does not exist: {index_path}")

    with index_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    if not headers:
        print("No headers found.")
        return 0

    needle = normalize(args.needle, args.case_sensitive)

    matches: list[str] = []
    total = 0
    for csv_row_num, row in enumerate(rows, start=2):
        parts = []
        for key in headers:
            text = str(row.get(key, "") or "")
            parts.append((key, text))

        searchable = " | ".join(text for _, text in parts)
        if needle in normalize(searchable, args.case_sensitive):
            total += 1
            rendered = " | ".join(f"{k}={v}" for k, v in parts)
            matches.append(f"{csv_row_num}: {rendered}")
            if len(matches) >= args.limit:
                break

    if total == 0:
        print(f"No matches for '{args.needle}' in {index_path}")
        return 0

    print(f"Matches for '{args.needle}' in {index_path} (showing up to {args.limit})")
    for line in matches:
        print(line)
    if total > len(matches):
        print(f"... and at least {total - len(matches)} more in scanned rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
