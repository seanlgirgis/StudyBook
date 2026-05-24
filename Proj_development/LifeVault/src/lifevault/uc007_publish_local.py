from __future__ import annotations

import csv
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .schema_v0 import MIGRATION_ID, validate_schema_v0
from .uc006_review import list_publish_readiness

REAL_DB_PATH = Path(r"D:\AI_Lab\LifeVault\db\lifevault.sqlite")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _check_db_ready(db_path: Path, real_db_confirm: bool) -> None:
    if db_path.resolve() == REAL_DB_PATH.resolve() and not real_db_confirm:
        raise ValueError(f"Refusing real DB path without --real-db-confirm: {db_path}")
    if not db_path.exists():
        raise FileNotFoundError(f"DB does not exist: {db_path}")
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        mig = conn.execute(
            "SELECT 1 FROM schema_migrations WHERE migration_id = ?", (MIGRATION_ID,)
        ).fetchone()
        if not mig:
            raise ValueError(f"Required migration missing: {MIGRATION_ID}")
        v = validate_schema_v0(conn)
        if not v["ok"]:
            raise ValueError(f"DB schema validation failed: {v}")


def _candidate_rows(db: Path, pod_id: str, limit: int = 5000) -> List[Dict[str, Any]]:
    readiness = list_publish_readiness(db, pod_id, limit=limit)
    rows = [r for r in readiness["items"] if r["readiness_status"] == "ready_to_publish"]
    return rows


def publish_to_local_vault(
    pod_id: str,
    db_path: str | Path,
    vault_root: str | Path,
    dry_run: bool = False,
    approved_publish: bool = False,
    real_db_confirm: bool = False,
) -> Dict[str, Any]:
    if dry_run and approved_publish:
        raise ValueError("Use either dry_run or approved_publish, not both")
    if not dry_run and not approved_publish:
        raise ValueError("Either dry_run or approved_publish flag is required")

    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=real_db_confirm)
    vr = Path(vault_root)
    pod_dest = vr / pod_id
    rows = _candidate_rows(db, pod_id)

    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        resolved: List[Dict[str, Any]] = []
        for r in rows:
            instance_id = r["instance_id"]
            src_row = conn.execute(
                "SELECT instance_path FROM file_instances WHERE instance_id = ? AND pod_id = ?",
                (instance_id, pod_id),
            ).fetchone()
            if not src_row:
                continue
            src = Path(src_row["instance_path"])
            dst = pod_dest / Path(r["filename"]).name
            resolved.append({**r, "source_path": str(src), "destination_path": str(dst)})

    summary = {
        "total_candidates": len(resolved),
        "intended_copy_count": len(resolved),
        "conflict_count": sum(1 for r in resolved if Path(r["destination_path"]).exists()),
    }
    if dry_run:
        return {
            "mode": "dry_run",
            "pod_id": pod_id,
            "db_path": str(db),
            "vault_root": str(vr),
            "summary": summary,
            "items": resolved,
            "writes": 0,
        }

    now = _now_iso()
    pod_dest.mkdir(parents=True, exist_ok=True)
    manifest_path = pod_dest / "_publish_manifest.csv"
    manifest_rows: List[Dict[str, Any]] = []
    copied = 0

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN")
        try:
            for r in resolved:
                src = Path(r["source_path"])
                dst = Path(r["destination_path"])
                status = "copied"
                err = ""
                if dst.exists():
                    status = "conflict_exists"
                    err = "Destination exists; overwrite refused."
                elif not src.exists():
                    status = "failed_missing_source"
                    err = "Source instance path does not exist."
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    copied += 1
                    conn.execute(
                        "UPDATE files SET publish_status = 'published', updated_at = ? WHERE file_id = (SELECT file_id FROM file_instances WHERE instance_id = ?)",
                        (now, r["instance_id"]),
                    )
                    conn.execute(
                        """
                        INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,decided_by,decision_note,created_at,updated_at)
                        VALUES(?, (SELECT file_id FROM file_instances WHERE instance_id = ?), 'approved', 'approved', 'published', 'uc007', ?, ?, ?)
                        """,
                        (
                            f"uc007_{pod_id}_{abs(hash((r['instance_id'], now))) & 0xFFFFFFFF:08x}",
                            r["instance_id"],
                            f"uc007_publish_local|pod_relative_path={r['pod_relative_path']}",
                            now,
                            now,
                        ),
                    )
                manifest_rows.append(
                    {
                        "pod_id": pod_id,
                        "instance_id": r["instance_id"],
                        "filename": r["filename"],
                        "pod_relative_path": r["pod_relative_path"],
                        "source_path": str(src),
                        "destination_path": str(dst),
                        "copy_status": status,
                        "copy_error": err,
                        "copied_at": now if status == "copied" else "",
                    }
                )

            conn.execute(
                """
                INSERT INTO audit_log(audit_id,event_type,event_time,actor,target_table,target_id,event_status,event_payload_json,created_at)
                VALUES(?, 'uc007_publish_local', ?, 'codex', 'pods', ?, ?, ?, ?)
                """,
                (
                    f"aud_uc007_{pod_id}_{now.replace(':', '').replace('-', '')}",
                    now,
                    pod_id,
                    "success",
                    json.dumps({"copied_count": copied, "candidate_count": len(resolved)}),
                    now,
                ),
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "instance_id",
                "filename",
                "pod_relative_path",
                "source_path",
                "destination_path",
                "copy_status",
                "copy_error",
                "copied_at",
            ],
        )
        w.writeheader()
        w.writerows(manifest_rows)

    return {
        "mode": "approved_publish",
        "pod_id": pod_id,
        "db_path": str(db),
        "vault_root": str(vr),
        "manifest_path": str(manifest_path),
        "copied_count": copied,
        "candidate_count": len(resolved),
        "writes": copied,
    }
