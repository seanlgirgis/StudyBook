from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List


def _open_read_only(db_path: str | Path) -> sqlite3.Connection:
    p = Path(db_path).resolve()
    uri = f"file:{p.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def list_pods(db_path: str | Path, limit: int = 50) -> List[Dict[str, Any]]:
    with _open_read_only(db_path) as conn:
        rows = conn.execute(
            """
            SELECT p.pod_id, p.pod_name, p.event_name, p.story_context, p.sensitivity_level,
                   p.created_at, s.source_name
            FROM pods p
            LEFT JOIN sources s ON s.source_id = p.source_id
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def search_metadata(
    db_path: str | Path,
    query: str | None = None,
    pod_id: str | None = None,
    filename_contains: str | None = None,
    extension: str | None = None,
    sensitivity_level: str | None = None,
    review_decision: str | None = None,
    vault_publish_status: str | None = None,
    project: str | None = None,
    category: str | None = None,
    event_name: str | None = None,
    duplicates_only: bool = False,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    sql = """
    SELECT
      f.file_id,
      f.filename,
      f.ext AS extension,
      f.sensitivity_level,
      p.pod_id,
      fi.instance_path AS pod_relative_path,
      s.root_ref AS source_path,
      rd.decision_type AS review_decision,
      f.publish_status AS vault_publish_status,
      (
        SELECT dgm2.duplicate_group_id
        FROM duplicate_group_members dgm2
        WHERE dgm2.file_id = f.file_id
        LIMIT 1
      ) AS duplicate_group_id
    FROM files f
    JOIN file_instances fi ON fi.file_id = f.file_id
    LEFT JOIN pods p ON p.pod_id = fi.pod_id
    LEFT JOIN sources s ON s.source_id = fi.source_id
    LEFT JOIN review_decisions rd ON rd.rowid = (
      SELECT r2.rowid
      FROM review_decisions r2
      WHERE r2.file_id = f.file_id
      ORDER BY r2.created_at DESC, r2.rowid DESC
      LIMIT 1
    )
    WHERE 1=1
    """
    params: List[Any] = []

    if pod_id:
        sql += " AND p.pod_id = ?"
        params.append(pod_id)
    if filename_contains:
        sql += " AND lower(f.filename) LIKE ?"
        params.append(f"%{filename_contains.lower()}%")
    if extension:
        sql += " AND lower(f.ext) = ?"
        params.append(extension.lower())
    if sensitivity_level:
        sql += " AND f.sensitivity_level = ?"
        params.append(sensitivity_level)
    if review_decision:
        sql += " AND rd.decision_type = ?"
        params.append(review_decision)
    if vault_publish_status:
        sql += " AND f.publish_status = ?"
        params.append(vault_publish_status)
    if event_name:
        sql += " AND p.event_name = ?"
        params.append(event_name)
    if query:
        sql += " AND (lower(f.filename) LIKE ? OR lower(coalesce(p.story_context,'')) LIKE ? OR lower(coalesce(p.pod_name,'')) LIKE ? OR lower(coalesce(p.event_name,'')) LIKE ?)"
        q = f"%{query.lower()}%"
        params.extend([q, q, q, q])
    if project:
        sql += " AND lower(coalesce(p.intake_notes,'')) LIKE ?"
        params.append(f"%{project.lower()}%")
    if category:
        sql += " AND lower(coalesce(p.intake_notes,'')) LIKE ?"
        params.append(f"%{category.lower()}%")
    if duplicates_only:
        sql += " AND EXISTS (SELECT 1 FROM duplicate_group_members dgm3 WHERE dgm3.file_id = f.file_id)"

    sql += " ORDER BY p.created_at DESC, f.filename ASC LIMIT ?"
    params.append(limit)

    with _open_read_only(db_path) as conn:
        rows = conn.execute(sql, tuple(params)).fetchall()
    out: List[Dict[str, Any]] = []
    for r in rows:
        d = dict(r)
        inst = (d.get("pod_relative_path") or "").replace("\\", "/")
        if inst:
            d["filename"] = Path(inst).name
        out.append(d)
    return out
