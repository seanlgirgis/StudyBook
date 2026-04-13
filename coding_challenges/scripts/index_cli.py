#!/usr/bin/env python3
"""
CSV-first index CLI for coding_challenges/index.csv.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = ROOT / "index.csv"
DEFAULT_HEADERS = ["id", "path", "primary", "tags", "title", "source"]


def parse_set_pairs(pairs: Iterable[str]) -> dict[str, str]:
    updates: dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise SystemExit(f"Invalid --set value '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit("Invalid --set value with empty key.")
        updates[key] = value
    return updates


def load_csv(index_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not index_path.exists():
        return list(DEFAULT_HEADERS), []

    with index_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or DEFAULT_HEADERS)
        rows = [{h: (row.get(h) or "") for h in headers} for row in reader]
    return headers, rows


def save_csv(index_path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})


def ensure_headers(headers: list[str], updates: dict[str, str]) -> list[str]:
    out = list(headers)
    for key in updates:
        if key not in out:
            out.append(key)
    return out


def render_row(row: dict[str, str], headers: list[str], row_num: int | None = None) -> str:
    parts = [f"{h}={row.get(h, '')}" for h in headers]
    prefix = f"{row_num}: " if row_num is not None else ""
    return prefix + " | ".join(parts)


def matches_row(
    row: dict[str, str],
    needle: str,
    headers: list[str],
    field: str | None,
    case_sensitive: bool,
) -> bool:
    if field:
        hay = row.get(field, "")
    else:
        hay = " | ".join(row.get(h, "") for h in headers)

    if case_sensitive:
        return needle in hay
    return needle.lower() in hay.lower()


def open_path(target: Path) -> None:
    if os.name == "nt":
        os.startfile(str(target))  # type: ignore[attr-defined]
        return
    subprocess.run(["xdg-open", str(target)], check=False)


def cmd_headers(args: argparse.Namespace) -> int:
    headers, _ = load_csv(args.index.resolve())
    print(" | ".join(headers))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    count = 0
    for i, row in enumerate(rows, start=2):
        print(render_row(row, headers, i))
        count += 1
        if count >= args.limit:
            break
    print(f"Displayed {count} rows from {index_path}")
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    if args.field and args.field not in headers:
        raise SystemExit(f"Unknown field '{args.field}'. Available: {', '.join(headers)}")

    count = 0
    for i, row in enumerate(rows, start=2):
        if matches_row(row, args.needle, headers, args.field, args.case_sensitive):
            print(render_row(row, headers, i))
            count += 1
            if count >= args.limit:
                break
    if count == 0:
        print(f"No matches for '{args.needle}' in {index_path}")
    else:
        print(f"Matched {count} row(s) in {index_path}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    hit = next((r for r in rows if r.get("id", "") == args.id), None)
    if not hit:
        raise SystemExit(f"id '{args.id}' not found in {index_path}")
    print(render_row(hit, headers))
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    if any(r.get("id", "") == args.id for r in rows):
        raise SystemExit(f"id '{args.id}' already exists in {index_path}")

    updates = parse_set_pairs(args.sets or [])
    updates["id"] = args.id
    updates["path"] = args.path
    headers = ensure_headers(headers, updates)

    row = {h: "" for h in headers}
    row.update(updates)
    rows.append(row)
    rows.sort(key=lambda r: (r.get("path", ""), r.get("id", "")))
    save_csv(index_path, headers, rows)
    print(f"Added id '{args.id}' to {index_path}")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    updates = parse_set_pairs(args.sets or [])
    if not updates:
        raise SystemExit("No updates provided. Use --set key=value.")

    match = next((r for r in rows if r.get("id", "") == args.id), None)
    if not match:
        raise SystemExit(f"id '{args.id}' not found in {index_path}")

    headers = ensure_headers(headers, updates)
    for key, value in updates.items():
        match[key] = value

    rows.sort(key=lambda r: (r.get("path", ""), r.get("id", "")))
    save_csv(index_path, headers, rows)
    print(f"Updated id '{args.id}' in {index_path}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    headers, rows = load_csv(index_path)
    before = len(rows)
    rows = [r for r in rows if r.get("id", "") != args.id]
    if len(rows) == before:
        raise SystemExit(f"id '{args.id}' not found in {index_path}")
    save_csv(index_path, headers, rows)
    print(f"Deleted id '{args.id}' from {index_path}")
    return 0


def cmd_open(args: argparse.Namespace) -> int:
    index_path = args.index.resolve()
    _, rows = load_csv(index_path)
    hit = next((r for r in rows if r.get("id", "") == args.id), None)
    if not hit:
        raise SystemExit(f"id '{args.id}' not found in {index_path}")

    rel = hit.get("path", "").strip()
    if not rel:
        raise SystemExit(f"id '{args.id}' has no path value.")

    target = ROOT / rel
    print(target)
    if args.print_only:
        return 0

    if not target.exists():
        raise SystemExit(f"Path does not exist: {target}")
    open_path(target)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage coding_challenges/index.csv")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH, help="Path to index CSV")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_headers = sub.add_parser("headers", help="Print CSV headers")
    p_headers.set_defaults(func=cmd_headers)

    p_list = sub.add_parser("list", help="List rows")
    p_list.add_argument("--limit", type=int, default=50)
    p_list.set_defaults(func=cmd_list)

    p_find = sub.add_parser("find", help="Find rows by substring")
    p_find.add_argument("needle")
    p_find.add_argument("--field", help="Limit search to one field")
    p_find.add_argument("--case-sensitive", action="store_true")
    p_find.add_argument("--limit", type=int, default=50)
    p_find.set_defaults(func=cmd_find)

    p_show = sub.add_parser("show", help="Show one row by id")
    p_show.add_argument("id")
    p_show.set_defaults(func=cmd_show)

    p_add = sub.add_parser("add", help="Add one row")
    p_add.add_argument("--id", required=True)
    p_add.add_argument("--path", required=True)
    p_add.add_argument("--set", dest="sets", action="append", help="Additional key=value fields")
    p_add.set_defaults(func=cmd_add)

    p_update = sub.add_parser("update", help="Update row fields by id")
    p_update.add_argument("id")
    p_update.add_argument("--set", dest="sets", action="append", required=True, help="key=value pair")
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a row by id")
    p_delete.add_argument("id")
    p_delete.set_defaults(func=cmd_delete)

    p_open = sub.add_parser("open", help="Open row path by id")
    p_open.add_argument("id")
    p_open.add_argument("--print-only", action="store_true", help="Print full resolved path only")
    p_open.set_defaults(func=cmd_open)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
