from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .schema_v0 import MIGRATION_ID, validate_schema_v0

REAL_DB_PATH = Path(r"D:\AI_Lab\LifeVault\db\lifevault.sqlite")
ALLOWED_DECISIONS = {
    "needs_review",
    "keep",
    "skip",
    "duplicate_keep",
    "duplicate_skip",
    "sensitive_review",
    "archive",
}


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


def _decision_to_status(decision: str) -> str:
    return {
        "needs_review": "needs_review",
        "keep": "approved",
        "skip": "skipped",
        "duplicate_keep": "duplicate_review",
        "duplicate_skip": "duplicate_review",
        "sensitive_review": "sensitive_review",
        "archive": "archive",
    }[decision]


def _build_decision_note(pod_relative_path: str, decision: str) -> str:
    return f"pod_relative_path={pod_relative_path}|decision_value={decision}"


def list_review_items(db_path: str | Path, pod_id: str, limit: int = 500) -> List[Dict[str, Any]]:
    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=True)
    sql = """
    SELECT
      fi.instance_id,
      fi.instance_path AS pod_relative_path,
      f.filename,
      f.ext AS extension,
      f.sensitivity_level,
      f.publish_status AS vault_publish_status,
      (
        SELECT rd.decision_type
        FROM review_decisions rd
        WHERE rd.file_id = fi.file_id
          AND rd.decision_note LIKE ('pod_relative_path=' || fi.instance_path || '|%')
        ORDER BY rd.created_at DESC, rd.rowid DESC
        LIMIT 1
      ) AS db_decision_type,
      (
        SELECT rd.decision_note
        FROM review_decisions rd
        WHERE rd.file_id = fi.file_id
          AND rd.decision_note LIKE ('pod_relative_path=' || fi.instance_path || '|%')
        ORDER BY rd.created_at DESC, rd.rowid DESC
        LIMIT 1
      ) AS db_decision_note,
      (
        SELECT rd.publish_status
        FROM review_decisions rd
        WHERE rd.file_id = fi.file_id
          AND rd.decision_note LIKE ('pod_relative_path=' || fi.instance_path || '|%')
        ORDER BY rd.created_at DESC, rd.rowid DESC
        LIMIT 1
      ) AS db_publish_status,
      (
        SELECT dgm.duplicate_group_id
        FROM duplicate_group_members dgm
        WHERE dgm.file_id = fi.file_id
        LIMIT 1
      ) AS duplicate_group_id
    FROM file_instances fi
    JOIN files f ON f.file_id = fi.file_id
    WHERE fi.pod_id = ?
    ORDER BY fi.instance_path ASC
    LIMIT ?
    """
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute(sql, (pod_id, limit)).fetchall()]
    for row in rows:
        row["filename"] = Path(row.get("pod_relative_path") or row.get("filename") or "").name
        row["decision"] = "needs_review"
        note = row.get("db_decision_note") or ""
        if "decision_value=" in note:
            row["decision"] = note.split("decision_value=", 1)[1].strip()
        elif row.get("db_decision_type"):
            row["decision"] = row["db_decision_type"]
    return rows


def list_duplicate_items(db_path: str | Path, pod_id: str, limit: int = 500) -> List[Dict[str, Any]]:
    return [
        r
        for r in list_review_items(db_path, pod_id, limit=limit)
        if r.get("duplicate_group_id")
    ]


def list_publish_readiness(db_path: str | Path, pod_id: str, limit: int = 500) -> Dict[str, Any]:
    rows = list_review_items(db_path, pod_id, limit=limit)
    readiness_rows: List[Dict[str, Any]] = []
    for row in rows:
        decision = row.get("decision") or "needs_review"
        sensitivity = row.get("sensitivity_level") or "unknown"
        publish_status = row.get("db_publish_status") or row.get("vault_publish_status")
        approved_for_vault_publish = publish_status == "publish_approved"

        if decision == "duplicate_skip":
            status = "blocked_duplicate_skip"
            reason = "Instance marked duplicate_skip."
        elif decision in {"needs_review", ""}:
            status = "blocked_needs_review"
            reason = "Review decision is needs_review or missing."
        elif decision == "sensitive_review":
            status = "blocked_sensitive_review"
            reason = "Item requires sensitive review before publish."
        elif decision == "skip":
            status = "blocked_skip"
            reason = "Instance marked skip."
        elif decision == "archive":
            status = "blocked_archive"
            reason = "Instance marked archive."
        elif decision in {"keep", "duplicate_keep"} and approved_for_vault_publish:
            status = "ready_to_publish"
            reason = "Decision allows publish and approval flag is true."
        elif sensitivity in {"sensitive", "highly_sensitive"} and not approved_for_vault_publish:
            status = "blocked_sensitive_review"
            reason = "Sensitive item is not approved_for_vault_publish."
        elif decision in {"keep", "duplicate_keep"} and not approved_for_vault_publish:
            status = "blocked_not_approved"
            reason = "Decision allows publish but approved_for_vault_publish is false."
        else:
            status = "blocked_needs_review"
            reason = "No publish-ready decision/approval combination found."

        readiness_rows.append(
            {
                "instance_id": row.get("instance_id"),
                "filename": row.get("filename"),
                "pod_relative_path": row.get("pod_relative_path"),
                "sensitivity_level": sensitivity,
                "decision": decision,
                "approved_for_vault_publish": approved_for_vault_publish,
                "vault_publish_status": publish_status,
                "readiness_status": status,
                "readiness_reason": reason,
                "duplicate_group_id": row.get("duplicate_group_id"),
            }
        )

    summary = {
        "total_items": len(readiness_rows),
        "ready_to_publish_count": sum(1 for r in readiness_rows if r["readiness_status"] == "ready_to_publish"),
        "blocked_count": sum(1 for r in readiness_rows if r["readiness_status"] != "ready_to_publish"),
        "needs_review_count": sum(1 for r in readiness_rows if r["readiness_status"] == "blocked_needs_review"),
        "duplicate_skip_count": sum(1 for r in readiness_rows if r["readiness_status"] == "blocked_duplicate_skip"),
        "sensitive_blocked_count": sum(1 for r in readiness_rows if r["readiness_status"] == "blocked_sensitive_review"),
    }
    return {"pod_id": pod_id, "summary": summary, "items": readiness_rows}


def update_review_item(
    db_path: str | Path,
    pod_id: str,
    pod_relative_path: str,
    decision: str | None = None,
    approved_for_vault_publish: bool | None = None,
    approved_update: bool = False,
    real_db_confirm: bool = False,
) -> Dict[str, Any]:
    if not approved_update:
        raise ValueError("DB write requires --approved-update")
    if decision is None and approved_for_vault_publish is None:
        raise ValueError("Provide at least one update: --decision and/or --approved-for-vault-publish")
    if decision is not None and decision not in ALLOWED_DECISIONS:
        raise ValueError(f"Invalid decision: {decision}")

    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=real_db_confirm)
    now = _now_iso()

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        file_row = conn.execute(
            """
            SELECT fi.file_id
            FROM file_instances fi
            WHERE fi.pod_id = ? AND fi.instance_path = ?
            LIMIT 1
            """,
            (pod_id, pod_relative_path),
        ).fetchone()
        if not file_row:
            raise ValueError(f"Pod instance not found for pod_id={pod_id} path={pod_relative_path}")

        file_id = file_row["file_id"]
        final_decision = decision or "needs_review"
        review_status = _decision_to_status(final_decision)
        publish_status = "publish_approved" if approved_for_vault_publish else "not_published"
        note = _build_decision_note(pod_relative_path, final_decision)

        decision_id = f"uc006_{pod_id}_{abs(hash((pod_relative_path, now))) & 0xFFFFFFFF:08x}"
        conn.execute(
            """
            INSERT INTO review_decisions(decision_id, file_id, decision_type, review_status, publish_status,
                                         decided_by, decision_note, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, 'sean', ?, ?, ?)
            """,
            (decision_id, file_id, review_status, review_status, publish_status, note, now, now),
        )
        conn.execute(
            """
            UPDATE files
            SET review_status = ?, publish_status = ?, updated_at = ?
            WHERE file_id = ?
            """,
            (review_status, publish_status, now, file_id),
        )
        conn.commit()

    return {
        "pod_id": pod_id,
        "pod_relative_path": pod_relative_path,
        "decision": final_decision,
        "approved_for_vault_publish": bool(approved_for_vault_publish),
        "status": "updated",
    }
