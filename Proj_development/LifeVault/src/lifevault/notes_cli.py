from __future__ import annotations

import argparse
import json

from .notes import create_note, create_note_folder, create_sensitive_note_phase0, list_note_folders, search_notes


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
    c.add_argument("--note-folder-path", default=None)

    cf = sub.add_parser("create-folder")
    cf.add_argument("--title", required=True)
    cf.add_argument("--story", default="")
    cf.add_argument("--tags", default="")
    cf.add_argument("--notes-root", required=True)

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--notes-root", required=True)

    lf = sub.add_parser("list-folders")
    lf.add_argument("--notes-root", required=True)

    sp0 = sub.add_parser("create-sensitive-phase0")
    sp0.add_argument("--title", required=True)
    sp0.add_argument("--public-hint", required=True)
    sp0.add_argument("--story", default="")
    sp0.add_argument("--tags", default="")
    sp0.add_argument("--demo-protected-body", required=True)
    sp0.add_argument("--notes-root", required=True)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "create":
            out = create_note(
                title=args.title,
                story=args.story,
                tags=args.tags,
                body=args.body,
                notes_root=args.notes_root,
                note_folder_path=args.note_folder_path,
                requested_filename=args.filename,
            )
            print(json.dumps(out, ensure_ascii=True))
            return 0
        if args.cmd == "create-folder":
            out = create_note_folder(
                title=args.title,
                story=args.story,
                tags=args.tags,
                notes_root=args.notes_root,
            )
            print(json.dumps(out, ensure_ascii=True))
            return 0
        if args.cmd == "list-folders":
            rows = list_note_folders(args.notes_root)
            print(f"rows={len(rows)}")
            for row in rows:
                print(json.dumps(row, ensure_ascii=True))
            return 0
        if args.cmd == "create-sensitive-phase0":
            out = create_sensitive_note_phase0(
                title=args.title,
                public_hint=args.public_hint,
                story=args.story,
                tags=args.tags,
                demo_protected_body=args.demo_protected_body,
                notes_root=args.notes_root,
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
