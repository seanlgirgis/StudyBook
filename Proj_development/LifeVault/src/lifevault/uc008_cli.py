from __future__ import annotations

import argparse
import json

from .uc008_verify_publish import verify_local_publish


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_008 Verify Local Vault Publish")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--pod-id", required=True)
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--approved-verify", action="store_true")
    parser.add_argument("--real-db-confirm", action="store_true")
    args = parser.parse_args(argv)
    try:
        out = verify_local_publish(
            pod_id=args.pod_id,
            db_path=args.db_path,
            vault_root=args.vault_root,
            dry_run=args.dry_run,
            approved_verify=args.approved_verify,
            real_db_confirm=args.real_db_confirm,
        )
    except Exception as exc:
        print(f"UC_008 failed: {exc}")
        return 2
    print(json.dumps(out, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
