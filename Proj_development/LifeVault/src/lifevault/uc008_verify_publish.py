from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .schema_v0 import MIGRATION_ID, validate_schema_v0

REAL_DB_PATH = Path(r"D:\AI_Lab\LifeVault\db\lifevault.sqlite")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def _read_publish_manifest(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Publish manifest not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if (r.get("copy_status") or "").strip() == "copied"]


def verify_local_publish(
    pod_id: str,
    db_path: str | Path,
    vault_root: str | Path,
    dry_run: bool = False,
    approved_verify: bool = False,
    real_db_confirm: bool = False,
) -> Dict[str, Any]:
    if dry_run and approved_verify:
        raise ValueError("Use either dry_run or approved_verify, not both")
    if not dry_run and not approved_verify:
        raise ValueError("Either dry_run or approved_verify flag is required")

    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=real_db_confirm)
    vr = Path(vault_root)
    pod_dir = vr / pod_id
    publish_manifest = pod_dir / "_publish_manifest.csv"
    verify_manifest = pod_dir / "_verify_manifest.csv"

    rows = _read_publish_manifest(publish_manifest)
    now = _now_iso()
    verified_rows: List[Dict[str, Any]] = []

    for r in rows:
        src = Path(r["source_path"])
        dst = Path(r["destination_path"])
        status = "verified"
        reason = ""
        src_sha = ""
        dst_sha = ""
        src_size = ""
        dst_size = ""
        if not src.exists():
            status = "failed_missing_source"
            reason = "Source path missing."
        elif not dst.exists():
            status = "failed_missing_destination"
            reason = "Destination path missing."
        else:
            src_size = str(src.stat().st_size)
            dst_size = str(dst.stat().st_size)
            if src_size != dst_size:
                status = "failed_size_mismatch"
                reason = "Size mismatch."
            else:
                src_sha = _sha256(src)
                dst_sha = _sha256(dst)
                if src_sha != dst_sha:
                    status = "failed_hash_mismatch"
                    reason = "SHA256 mismatch."
        verified_rows.append(
            {
                "pod_id": pod_id,
                "instance_id": r.get("instance_id", ""),
                "filename": r.get("filename", ""),
                "source_path": str(src),
                "destination_path": str(dst),
                "source_size": src_size,
                "destination_size": dst_size,
                "source_sha256": src_sha,
                "destination_sha256": dst_sha,
                "verify_status": status,
                "verify_reason": reason,
                "verified_at": now if status == "verified" else "",
            }
        )

    summary = {
        "total_rows": len(verified_rows),
        "verified_count": sum(1 for r in verified_rows if r["verify_status"] == "verified"),
        "failed_count": sum(1 for r in verified_rows if r["verify_status"] != "verified"),
    }
    if dry_run:
        return {
            "mode": "dry_run",
            "pod_id": pod_id,
            "db_path": str(db),
            "vault_root": str(vr),
            "verify_manifest_path": str(verify_manifest),
            "summary": summary,
            "writes": 0,
        }

    pod_dir.mkdir(parents=True, exist_ok=True)
    with verify_manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "instance_id",
                "filename",
                "source_path",
                "destination_path",
                "source_size",
                "destination_size",
                "source_sha256",
                "destination_sha256",
                "verify_status",
                "verify_reason",
                "verified_at",
            ],
        )
        w.writeheader()
        w.writerows(verified_rows)

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN")
        try:
            for row in verified_rows:
                if row["verify_status"] != "verified":
                    continue
                inst_id = row["instance_id"]
                conn.execute(
                    "UPDATE files SET publish_status='verified', updated_at=? WHERE file_id=(SELECT file_id FROM file_instances WHERE instance_id=?)",
                    (now, inst_id),
                )
                conn.execute(
                    """
                    INSERT INTO review_decisions(decision_id,file_id,decision_type,review_status,publish_status,decided_by,decision_note,created_at,updated_at)
                    VALUES(?, (SELECT file_id FROM file_instances WHERE instance_id = ?), 'approved', 'approved', 'verified', 'uc008', ?, ?, ?)
                    """,
                    (
                        f"uc008_{pod_id}_{abs(hash((inst_id, now))) & 0xFFFFFFFF:08x}",
                        inst_id,
                        "uc008_verify_local_publish",
                        now,
                        now,
                    ),
                )
            conn.execute(
                """
                INSERT INTO audit_log(audit_id,event_type,event_time,actor,target_table,target_id,event_status,event_payload_json,created_at)
                VALUES(?, 'uc008_verify_publish', ?, 'codex', 'pods', ?, ?, ?, ?)
                """,
                (
                    f"aud_uc008_{pod_id}_{now.replace(':', '').replace('-', '')}",
                    now,
                    pod_id,
                    "success",
                    json.dumps(summary),
                    now,
                ),
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    return {
        "mode": "approved_verify",
        "pod_id": pod_id,
        "db_path": str(db),
        "vault_root": str(vr),
        "verify_manifest_path": str(verify_manifest),
        "summary": summary,
        "writes": summary["verified_count"],
    }
