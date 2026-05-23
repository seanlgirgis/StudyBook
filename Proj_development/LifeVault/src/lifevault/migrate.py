from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

from .schema_v0 import MIGRATION_ID, apply_schema_v0, validate_schema_v0

REAL_DB_PATH = Path(r"D:\AI_Lab\LifeVault\db\lifevault.sqlite")
REPO_ROOT = Path(__file__).resolve().parents[2]


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _validate_path_guards(db_path: Path, real_db_confirm: bool) -> None:
    if db_path.resolve() == REAL_DB_PATH.resolve() and not real_db_confirm:
        raise ValueError(
            "Refusing real DB path without --real-db-confirm: "
            f"{REAL_DB_PATH}"
        )
    if _is_inside(db_path, REPO_ROOT):
        raise ValueError(f"Refusing DB path inside repo root: {db_path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LifeVault migration runner")
    parser.add_argument("--db-path", required=True, help="SQLite DB path")
    parser.add_argument("--apply", help="Migration ID to apply")
    parser.add_argument("--status", action="store_true", help="Show migration status")
    parser.add_argument("--validate", action="store_true", help="Validate schema")
    parser.add_argument("--dry-run", action="store_true", help="Show intended action")
    parser.add_argument(
        "--real-db-confirm",
        action="store_true",
        help="Required to target real operational DB path",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    action_count = sum(
        [
            1 if args.apply else 0,
            1 if args.status else 0,
            1 if args.validate else 0,
            1 if args.dry_run else 0,
        ]
    )
    if action_count != 1:
        print("Error: specify exactly one action (--apply/--status/--validate/--dry-run)")
        return 2

    db_path = Path(args.db_path)

    try:
        _validate_path_guards(db_path, args.real_db_confirm)
    except ValueError as exc:
        print(f"Unsafe path rejected: {exc}")
        return 3

    if args.dry_run:
        exists = db_path.exists()
        print(f"DRY-RUN: action={'apply ' + args.apply if args.apply else 'inspection'}")
        print(f"DRY-RUN: target_db_path={db_path}")
        print(f"DRY-RUN: db_exists={exists}")
        print("DRY-RUN: no changes written")
        return 0

    if args.apply:
        if args.apply != MIGRATION_ID:
            print(f"Unsupported migration id: {args.apply}")
            return 2

        db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            result = apply_schema_v0(conn)
            validation = result["validation"]
            if not validation["ok"]:
                print(f"Apply failed validation: {validation}")
                return 4
            if result["already_applied"]:
                print(f"Migration already applied and valid: {MIGRATION_ID}")
            else:
                print(f"Migration applied successfully: {MIGRATION_ID}")
        return 0

    if args.status:
        if not db_path.exists():
            print("Status: database does not exist")
            return 0
        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'"
            ).fetchone()
            if not row:
                print("Status: schema_migrations table missing")
                return 0
            mig = conn.execute(
                "SELECT applied_at FROM schema_migrations WHERE migration_id = ?",
                (MIGRATION_ID,),
            ).fetchone()
            if mig:
                print(f"Status: {MIGRATION_ID} applied at {mig[0]}")
            else:
                print(f"Status: {MIGRATION_ID} not applied")
        return 0

    if args.validate:
        if not db_path.exists():
            print("Validation failed: database does not exist")
            return 4
        with sqlite3.connect(db_path) as conn:
            validation = validate_schema_v0(conn)
        if validation["ok"]:
            print("Validation passed")
            return 0
        print(f"Validation failed: {validation}")
        return 4

    return 2


if __name__ == "__main__":
    raise SystemExit(main())