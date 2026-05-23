from __future__ import annotations

import argparse
import json

from .uc005_search import list_pods, search_metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_005 Search Memory Without Hydration")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--query", default=None)
    parser.add_argument("--pod-id", default=None)
    parser.add_argument("--filename-contains", default=None)
    parser.add_argument("--extension", default=None)
    parser.add_argument("--sensitivity", default=None)
    parser.add_argument("--review-decision", default=None)
    parser.add_argument("--vault-publish-status", default=None)
    parser.add_argument("--project", default=None)
    parser.add_argument("--category", default=None)
    parser.add_argument("--event-name", default=None)
    parser.add_argument("--duplicates-only", action="store_true")
    parser.add_argument("--list-pods", action="store_true")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)

    try:
        if args.list_pods:
            rows = list_pods(args.db_path, limit=args.limit)
        else:
            rows = search_metadata(
                db_path=args.db_path,
                query=args.query,
                pod_id=args.pod_id,
                filename_contains=args.filename_contains,
                extension=args.extension,
                sensitivity_level=args.sensitivity,
                review_decision=args.review_decision,
                vault_publish_status=args.vault_publish_status,
                project=args.project,
                category=args.category,
                event_name=args.event_name,
                duplicates_only=args.duplicates_only,
                limit=args.limit,
            )
    except Exception as exc:
        print(f"UC_005 failed: {exc}")
        return 2

    print(f"rows={len(rows)}")
    for row in rows:
        print(json.dumps(row, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())