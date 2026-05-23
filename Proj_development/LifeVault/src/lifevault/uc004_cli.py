from __future__ import annotations

import argparse

from .uc004_index_pod import index_pod_to_database


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_004 Index Pod to Database")
    parser.add_argument("--pod-path", required=True)
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--approved", action="store_true")
    parser.add_argument("--real-db-confirm", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = index_pod_to_database(
            pod_path=args.pod_path,
            db_path=args.db_path,
            approved=args.approved,
            dry_run=args.dry_run,
            real_db_confirm=args.real_db_confirm,
        )
    except Exception as exc:
        print(f"UC_004 failed: {exc}")
        return 2

    print(f"UC_004 mode={result['mode']}")
    print(f"pod_id={result['pod_id']}")
    print(f"db_path={result['db_path']}")
    print(f"summary={result['summary']}")
    print(f"writes={result['writes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
