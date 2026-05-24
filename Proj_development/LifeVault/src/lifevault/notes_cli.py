from __future__ import annotations

import argparse
import json

from .notes import create_note, search_notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LifeVault Notes v0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--story", default="")
    c.add_argument("--tags", default="")
    c.add_argument("--body", default="")
    c.add_argument("--notes-root", required=True)
    c.add_argument("--filename", default=None)

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--notes-root", required=True)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "create":
            out = create_note(
                title=args.title,
                story=args.story,
                tags=args.tags,
                body=args.body,
                notes_root=args.notes_root,
                requested_filename=args.filename,
            )
            print(json.dumps(out, ensure_ascii=True))
            return 0
        rows = search_notes(args.notes_root, args.query)
        print(f"rows={len(rows)}")
        for row in rows:
            print(json.dumps(row, ensure_ascii=True))
        return 0
    except Exception as exc:
        print(f"notes_cli failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
