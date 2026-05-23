from __future__ import annotations

import argparse
import json

from .uc006_review import (
    list_duplicate_items,
    list_publish_readiness,
    list_review_items,
    update_review_item,
)


def _parse_bool(text: str | None) -> bool | None:
    if text is None:
        return None
    v = text.strip().lower()
    if v in {"true", "1", "yes"}:
        return True
    if v in {"false", "0", "no"}:
        return False
    raise ValueError("--approved-for-vault-publish must be true/false")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_006 Review and Decide Pod Items")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--pod-id", required=True)
    parser.add_argument("--list-items", action="store_true")
    parser.add_argument("--list-duplicates", action="store_true")
    parser.add_argument("--publish-readiness", action="store_true")
    parser.add_argument("--pod-relative-path", default=None)
    parser.add_argument("--decision", default=None)
    parser.add_argument("--approved-for-vault-publish", default=None)
    parser.add_argument("--approved-update", action="store_true")
    parser.add_argument("--real-db-confirm", action="store_true")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args(argv)

    try:
        if args.list_items:
            rows = list_review_items(args.db_path, args.pod_id, limit=args.limit)
            print(f"rows={len(rows)}")
            for row in rows:
                print(json.dumps(row, ensure_ascii=True))
            return 0
        if args.list_duplicates:
            rows = list_duplicate_items(args.db_path, args.pod_id, limit=args.limit)
            print(f"rows={len(rows)}")
            for row in rows:
                print(json.dumps(row, ensure_ascii=True))
            return 0
        if args.publish_readiness:
            out = list_publish_readiness(args.db_path, args.pod_id, limit=args.limit)
            print(json.dumps(out["summary"], ensure_ascii=True))
            print(f"rows={len(out['items'])}")
            for row in out["items"]:
                print(json.dumps(row, ensure_ascii=True))
            return 0
        if not args.pod_relative_path:
            raise ValueError("--pod-relative-path is required for updates")
        approved_publish = _parse_bool(args.approved_for_vault_publish)
        out = update_review_item(
            db_path=args.db_path,
            pod_id=args.pod_id,
            pod_relative_path=args.pod_relative_path,
            decision=args.decision,
            approved_for_vault_publish=approved_publish,
            approved_update=args.approved_update,
            real_db_confirm=args.real_db_confirm,
        )
        print(json.dumps(out, ensure_ascii=True))
        return 0
    except Exception as exc:
        print(f"UC_006 failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
