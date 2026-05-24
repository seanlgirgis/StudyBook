from __future__ import annotations

import csv
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .schema_v0 import MIGRATION_ID, validate_schema_v0
from .uc006_review import list_review_items

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


def _is_candidate_decision(decision: str) -> bool:
    return decision in {"duplicate_skip", "skip", "archive"}


def _collect_candidates(
    db: Path, pod_id: str, include_sensitive: bool, limit: int = 5000
) -> List[Dict[str, Any]]:
    items = list_review_items(db, pod_id, limit=limit)
    by_instance_id = {r.get("instance_id"): r for r in items}

    def _has_verified_keep_peer(row: Dict[str, Any]) -> bool:
        gid = row.get("duplicate_group_id")
        if not gid:
            return False
        this_instance = row.get("instance_id")
        for peer in items:
            if peer.get("instance_id") == this_instance:
                continue
            if peer.get("duplicate_group_id") != gid:
                continue
            if (peer.get("decision") or "needs_review") != "duplicate_keep":
                continue
            db_pub = (peer.get("db_publish_status") or "").lower()
            file_pub = (peer.get("vault_publish_status") or "").lower()
            if db_pub == "verified" or file_pub == "verified":
                return True
        return False

    candidates: List[Dict[str, Any]] = []
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        for r in items:
            decision = r.get("decision") or "needs_review"
            if not _is_candidate_decision(decision):
                continue
            sens = (r.get("sensitivity_level") or "unknown").lower()
            if sens in {"sensitive", "highly_sensitive"} and not include_sensitive:
                continue
            inst_id = r["instance_id"]
            inst_row = conn.execute(
                "SELECT file_id, instance_path FROM file_instances WHERE instance_id = ? AND pod_id = ?",
                (inst_id, pod_id),
            ).fetchone()
            if not inst_row:
                continue
            file_id = inst_row["file_id"]
            src_path = Path(inst_row["instance_path"])

            if decision == "duplicate_skip":
                if not _has_verified_keep_peer(r):
                    continue

            candidates.append(
                {
                    "instance_id": inst_id,
                    "file_id": file_id,
                    "filename": Path(r.get("pod_relative_path") or r.get("filename") or "").name,
                    "source_path": str(src_path),
                    "decision": decision,
                    "sensitivity_level": sens,
                }
            )
    return candidates


def cleanup_to_quarantine(
    pod_id: str,
    db_path: str | Path,
    quarantine_root: str | Path,
    dry_run: bool = False,
    approved_cleanup: bool = False,
    real_db_confirm: bool = False,
    include_sensitive: bool = False,
) -> Dict[str, Any]:
    if dry_run and approved_cleanup:
        raise ValueError("Use either dry_run or approved_cleanup, not both")
    if not dry_run and not approved_cleanup:
        raise ValueError("Either dry_run or approved_cleanup flag is required")

    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=real_db_confirm)
    qr = Path(quarantine_root)
    pod_q = qr / pod_id
    candidates = _collect_candidates(db, pod_id, include_sensitive=include_sensitive)

    resolved: List[Dict[str, Any]] = []
    for c in candidates:
        dst = pod_q / Path(c["filename"]).name
        resolved.append({**c, "destination_path": str(dst)})

    summary = {
        "candidate_count": len(resolved),
        "conflict_count": sum(1 for r in resolved if Path(r["destination_path"]).exists()),
    }
    if dry_run:
        return {
            "mode": "dry_run",
            "pod_id": pod_id,
            "db_path": str(db),
            "quarantine_root": str(qr),
            "summary": summary,
            "items": resolved,
            "writes": 0,
        }

    now = _now_iso()
    pod_q.mkdir(parents=True, exist_ok=True)
    manifest = pod_q / "_cleanup_manifest.csv"
    manifest_rows: List[Dict[str, Any]] = []
    moved = 0

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN")
        try:
            for r in resolved:
                src = Path(r["source_path"])
                dst = Path(r["destination_path"])
                status = "quarantined"
                err = ""
                if dst.exists():
                    status = "conflict_exists"
                    err = "Destination exists; overwrite refused."
                elif not src.exists():
                    status = "failed_missing_source"
                    err = "Source file missing."
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    moved += 1

                manifest_rows.append(
                    {
                        "pod_id": pod_id,
                        "instance_id": r["instance_id"],
                        "file_id": r["file_id"],
                        "filename": r["filename"],
                        "source_path": str(src),
                        "quarantine_path": str(dst),
                        "decision": r["decision"],
                        "cleanup_status": status,
                        "cleanup_error": err,
                        "cleaned_at": now if status == "quarantined" else "",
                    }
                )

            conn.execute(
                """
                INSERT INTO audit_log(audit_id,event_type,event_time,actor,target_table,target_id,event_status,event_payload_json,created_at)
                VALUES(?, 'uc009_cleanup_quarantine', ?, 'codex', 'pods', ?, ?, ?, ?)
                """,
                (
                    f"aud_uc009_{pod_id}_{now.replace(':', '').replace('-', '')}",
                    now,
                    pod_id,
                    "success",
                    json.dumps({"moved_count": moved, "candidate_count": len(resolved)}),
                    now,
                ),
            )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    with manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "pod_id",
                "instance_id",
                "file_id",
                "filename",
                "source_path",
                "quarantine_path",
                "decision",
                "cleanup_status",
                "cleanup_error",
                "cleaned_at",
            ],
        )
        w.writeheader()
        w.writerows(manifest_rows)

    return {
        "mode": "approved_cleanup",
        "pod_id": pod_id,
        "db_path": str(db),
        "quarantine_root": str(qr),
        "manifest_path": str(manifest),
        "moved_count": moved,
        "candidate_count": len(resolved),
        "writes": moved,
    }
