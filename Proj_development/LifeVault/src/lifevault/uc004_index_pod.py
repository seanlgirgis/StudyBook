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


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _required_artifacts(pod_path: Path) -> Dict[str, Path]:
    files = {
        "profile": pod_path / "_pod_profile.json",
        "manifest": pod_path / "_pod_manifest.csv",
        "review": pod_path / "_review.csv",
        "snapshot": pod_path / "_source_proposal_snapshot.json",
    }
    missing = [k for k, v in files.items() if not v.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required pod artifacts: {', '.join(missing)}")
    return files


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _check_db_ready(db_path: Path, real_db_confirm: bool = False) -> None:
    if db_path.resolve() == REAL_DB_PATH.resolve() and not real_db_confirm:
        raise ValueError("Real DB path is rejected in this bite; temp DB only")
    if not db_path.exists():
        raise FileNotFoundError(f"DB does not exist: {db_path}")

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        has_migration_table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'"
        ).fetchone()
        if not has_migration_table:
            raise ValueError("DB missing schema_migrations; required migration not applied")

        v = validate_schema_v0(conn)
        if not v["ok"]:
            raise ValueError(f"DB schema validation failed: {v}")
        mig = conn.execute(
            "SELECT 1 FROM schema_migrations WHERE migration_id = ?", (MIGRATION_ID,)
        ).fetchone()
        if not mig:
            raise ValueError(f"Required migration missing: {MIGRATION_ID}")


def index_pod_to_database(
    pod_path: str | Path,
    db_path: str | Path,
    approved: bool = False,
    dry_run: bool = False,
    real_db_confirm: bool = False,
) -> Dict[str, Any]:
    if dry_run and approved:
        raise ValueError("Use either dry_run or approved, not both")
    if not dry_run and not approved:
        raise ValueError("Either dry_run or approved flag is required")

    pod = Path(pod_path)
    if not pod.exists() or not pod.is_dir():
        raise FileNotFoundError(f"Pod path not found: {pod}")

    artifacts = _required_artifacts(pod)
    profile = _load_json(artifacts["profile"])
    snapshot = _load_json(artifacts["snapshot"])
    manifest_rows = _read_csv(artifacts["manifest"])
    review_rows = _read_csv(artifacts["review"])

    db = Path(db_path)
    _check_db_ready(db, real_db_confirm=real_db_confirm)

    pod_id = profile.get("pod_id") or pod.name
    source_path = profile.get("source_path") or snapshot.get("source_path")
    source_name = Path(source_path).name if source_path else "unknown_source"
    source_id = f"src_{hashlib.sha1(str(source_path).encode('utf-8')).hexdigest()[:12]}"

    duplicate_groups = set()
    for r in manifest_rows:
        gid = (r.get("duplicate_name_group_id") or "").strip()
        if gid:
            duplicate_groups.add(gid)

    summary = {
        "source_count": 1,
        "pod_count": 1,
        "file_count": len(manifest_rows),
        "file_instance_count": len(manifest_rows),
        "review_decision_count": len(review_rows),
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_member_count": len([r for r in manifest_rows if (r.get("duplicate_name_group_id") or "").strip()]),
    }

    if dry_run:
        return {
            "mode": "dry_run",
            "pod_id": pod_id,
            "db_path": str(db),
            "summary": summary,
            "writes": 0,
        }

    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        existing = conn.execute("SELECT 1 FROM pods WHERE pod_id = ?", (pod_id,)).fetchone()
        if existing:
            raise ValueError(f"pod_id already indexed: {pod_id}")

        now = _now_iso()

        conn.execute("BEGIN")
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO sources(source_id, source_type, source_name, root_ref, description, is_active, created_at)
                VALUES(?, 'local_folder', ?, ?, ?, 1, ?)
                """,
                (source_id, source_name, source_path, "UC_004 indexed source", now),
            )

            conn.execute(
                """
                INSERT INTO pods(pod_id, source_id, pod_name, event_name, pod_status, story_context, intake_notes,
                                 sensitivity_level, storage_temperature, created_at, updated_at)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pod_id,
                    source_id,
                    pod_id,
                    profile.get("event_name") or "initial_intake",
                    "onboarded_needs_review",
                    profile.get("story") or "",
                    profile.get("notes") or "",
                    profile.get("sensitivity_highest_level") or "unknown",
                    "warm",
                    profile.get("created_at") or now,
                    now,
                ),
            )

            file_id_by_pod_rel: Dict[str, str] = {}
            for i, row in enumerate(manifest_rows, start=1):
                pod_abs = Path(row["pod_absolute_path"])
                sha = _sha256(pod_abs)
                file_id = f"file_{sha[:16]}"
                file_id_by_pod_rel[row["pod_relative_path"]] = file_id

                conn.execute(
                    """
                    INSERT OR IGNORE INTO files(file_id, sha256, hash_algo, filename, ext, size_bytes, mime_type,
                                                file_status, review_status, publish_status, sensitivity_level,
                                                storage_temperature, created_at, updated_at)
                    VALUES(?, ?, 'sha256', ?, ?, ?, ?, 'copied_to_pod', 'needs_review', 'not_published', ?, 'warm', ?, ?)
                    """,
                    (
                        file_id,
                        sha,
                        row.get("filename"),
                        row.get("extension"),
                        int(row.get("size_bytes") or 0),
                        None,
                        row.get("filename_sensitivity_level") or "unknown",
                        now,
                        now,
                    ),
                )

                inst_id = f"inst_{pod_id}_{i:05d}"
                conn.execute(
                    """
                    INSERT INTO file_instances(instance_id, file_id, source_id, pod_id, instance_role, instance_path,
                                               path_is_absolute, path_platform, observed_at, is_current, created_at, updated_at)
                    VALUES(?, ?, ?, ?, 'pod_copy', ?, 1, 'windows', ?, 1, ?, ?)
                    """,
                    (inst_id, file_id, source_id, pod_id, row.get("pod_absolute_path"), now, now, now),
                )

            for j, rr in enumerate(review_rows, start=1):
                pod_rel = rr.get("pod_relative_path") or ""
                file_id = file_id_by_pod_rel.get(pod_rel)
                if not file_id:
                    continue
                decision_id = f"rev_{pod_id}_{j:05d}"
                decision_type = rr.get("review_decision") or "needs_review"
                if decision_type not in {
                    "needs_review",
                    "approved",
                    "skipped",
                    "duplicate_review",
                    "sensitive_review",
                    "archive",
                }:
                    raise ValueError(f"Invalid review_decision in review CSV: {decision_type}")

                conn.execute(
                    """
                    INSERT INTO review_decisions(decision_id, file_id, decision_type, review_status, publish_status,
                                                 decided_by, decision_note, created_at, updated_at)
                    VALUES(?, ?, ?, ?, 'not_published', NULL, ?, ?, ?)
                    """,
                    (decision_id, file_id, decision_type, decision_type, rr.get("user_notes") or "", now, now),
                )

            for gid in sorted(duplicate_groups):
                instance_count = len(
                    [
                        r
                        for r in manifest_rows
                        if (r.get("duplicate_name_group_id") or "").strip() == gid
                    ]
                )
                file_member_ids = {
                    file_id_by_pod_rel[row.get("pod_relative_path", "")]
                    for row in manifest_rows
                    if (row.get("duplicate_name_group_id") or "").strip() == gid
                    and row.get("pod_relative_path", "") in file_id_by_pod_rel
                }
                conn.execute(
                    """
                    INSERT OR IGNORE INTO duplicate_groups(duplicate_group_id, group_method, group_status, confidence_score,
                                                           note, created_at, updated_at)
                    VALUES(?, 'duplicate_name_candidate', 'open', NULL, NULL, ?, ?)
                    """,
                    (gid, now, now),
                )
                conn.execute(
                    """
                    UPDATE duplicate_groups
                    SET note = ?, updated_at = ?
                    WHERE duplicate_group_id = ?
                    """,
                    (
                        f"instance_count={instance_count};unique_file_count={len(file_member_ids)}",
                        now,
                        gid,
                    ),
                )
                for pod_rel, file_id in file_id_by_pod_rel.items():
                    for row in manifest_rows:
                        if row.get("pod_relative_path") == pod_rel and (row.get("duplicate_name_group_id") or "").strip() == gid:
                            conn.execute(
                                """
                                INSERT OR IGNORE INTO duplicate_group_members(duplicate_group_id, file_id, member_role,
                                                                              is_canonical_candidate, created_at)
                                VALUES(?, ?, 'candidate', 0, ?)
                                """,
                                (gid, file_id, now),
                            )

            conn.execute(
                """
                INSERT INTO audit_log(audit_id, event_type, event_time, actor, target_table, target_id,
                                      event_status, event_payload_json, created_at)
                VALUES(?, 'uc004_index_pod', ?, 'codex', 'pods', ?, 'success', ?, ?)
                """,
                (
                    f"aud_{pod_id}_{now.replace(':', '').replace('-', '')}",
                    now,
                    pod_id,
                    json.dumps({"mode": "approved", "summary": summary}),
                    now,
                ),
            )

            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

    return {
        "mode": "approved",
        "pod_id": pod_id,
        "db_path": str(db),
        "summary": summary,
        "writes": sum(summary.values()),
    }
