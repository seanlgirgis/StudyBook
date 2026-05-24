from __future__ import annotations

import argparse
import json

from .uc009_cleanup_quarantine import cleanup_to_quarantine


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_009 Cleanup Source After Verification (Quarantine)")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--pod-id", required=True)
    parser.add_argument("--quarantine-root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--approved-cleanup", action="store_true")
    parser.add_argument("--real-db-confirm", action="store_true")
    parser.add_argument("--include-sensitive", action="store_true")
    args = parser.parse_args(argv)
    try:
        out = cleanup_to_quarantine(
            pod_id=args.pod_id,
            db_path=args.db_path,
            quarantine_root=args.quarantine_root,
            dry_run=args.dry_run,
            approved_cleanup=args.approved_cleanup,
            real_db_confirm=args.real_db_confirm,
            include_sensitive=args.include_sensitive,
        )
    except Exception as exc:
        print(f"UC_009 failed: {exc}")
        return 2
    print(json.dumps(out, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
