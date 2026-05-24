from __future__ import annotations

import argparse
import json

from .uc007_publish_local import publish_to_local_vault


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_007 Publish Approved Files to Local Vault")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--pod-id", required=True)
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--approved-publish", action="store_true")
    parser.add_argument("--real-db-confirm", action="store_true")
    args = parser.parse_args(argv)

    try:
        out = publish_to_local_vault(
            pod_id=args.pod_id,
            db_path=args.db_path,
            vault_root=args.vault_root,
            dry_run=args.dry_run,
            approved_publish=args.approved_publish,
            real_db_confirm=args.real_db_confirm,
        )
    except Exception as exc:
        print(f"UC_007 failed: {exc}")
        return 2

    print(json.dumps(out, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
