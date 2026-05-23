from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Mapping

from .config import load_config


def db_path() -> Path:
    cfg = load_config()
    p = cfg.lab_path("db_dir") / "onedriveclean.sqlite"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def connect_db(path: Path | None = None) -> sqlite3.Connection:
    target = path or db_path()
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS pods (
          pod_id TEXT PRIMARY KEY,
          pod_name TEXT,
          source_path TEXT,
          project TEXT,
          category TEXT,
          event_name TEXT,
          suggested_vault_path TEXT,
          status TEXT,
          created_at TEXT,
          notes TEXT
        );

        CREATE TABLE IF NOT EXISTS files (
          file_id INTEGER PRIMARY KEY AUTOINCREMENT,
          pod_id TEXT,
          batch_name TEXT,
          source_name TEXT,
          source_path TEXT NOT NULL,
          staged_path TEXT,
          filename TEXT NOT NULL,
          extension TEXT,
          size_bytes INTEGER,
          modified_time TEXT,
          project TEXT,
          category TEXT,
          event_name TEXT,
          suggested_vault_path TEXT,
          suggested_clean_remote_path TEXT,
          approved_clean_remote_path TEXT,
          copy_status TEXT,
          text_extraction_status TEXT,
          notes TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS batches (
          batch_name TEXT PRIMARY KEY,
          source_name TEXT,
          project TEXT,
          category TEXT,
          suggested_clean_remote_path TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          notes TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_files_filename ON files(filename);
        CREATE INDEX IF NOT EXISTS idx_files_project ON files(project);
        CREATE INDEX IF NOT EXISTS idx_files_category ON files(category);
        CREATE INDEX IF NOT EXISTS idx_files_pod_id ON files(pod_id);
        """
    )
    conn.commit()


def upsert_pod(conn: sqlite3.Connection, pod: Mapping[str, str]) -> None:
    conn.execute(
        """
        INSERT INTO pods(pod_id, pod_name, source_path, project, category, event_name, suggested_vault_path, status, created_at, notes)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(pod_id) DO UPDATE SET
          pod_name=excluded.pod_name,
          source_path=excluded.source_path,
          project=excluded.project,
          category=excluded.category,
          event_name=excluded.event_name,
          suggested_vault_path=excluded.suggested_vault_path,
          status=excluded.status,
          notes=excluded.notes
        """,
        (
            pod.get("pod_id"),
            pod.get("pod_name"),
            pod.get("source_path"),
            pod.get("project"),
            pod.get("category"),
            pod.get("event_name"),
            pod.get("suggested_vault_path"),
            pod.get("status"),
            pod.get("created_at"),
            pod.get("notes"),
        ),
    )
    conn.commit()


def upsert_files_from_manifest(conn: sqlite3.Connection, rows: Iterable[Mapping[str, str]]) -> int:
    count = 0
    for r in rows:
        conn.execute(
            """
            INSERT OR REPLACE INTO files(
              file_id, pod_id, batch_name, source_name, source_path, staged_path, filename, extension,
              size_bytes, modified_time, project, category, event_name, suggested_vault_path,
              suggested_clean_remote_path, approved_clean_remote_path, copy_status, text_extraction_status, notes
            ) VALUES (
              (SELECT file_id FROM files WHERE pod_id=? AND staged_path=?),
              ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
              COALESCE((SELECT approved_clean_remote_path FROM files WHERE pod_id=? AND staged_path=?), NULL),
              COALESCE((SELECT copy_status FROM files WHERE pod_id=? AND staged_path=?), NULL),
              COALESCE(?, 'not_extracted'),
              COALESCE((SELECT notes FROM files WHERE pod_id=? AND staged_path=?), NULL)
            )
            """,
            (
                r.get("pod_id"), r.get("pod_file_path") or r.get("staged_path"),
                r.get("pod_id"),
                r.get("batch_name"),
                r.get("source_name"),
                r.get("source_file_path") or r.get("source_path"),
                r.get("pod_file_path") or r.get("staged_path"),
                r.get("filename"),
                r.get("extension"),
                int(r.get("size_bytes", 0) or 0),
                r.get("modified_time"),
                r.get("project"),
                r.get("category"),
                r.get("event_name"),
                r.get("suggested_vault_path") or r.get("suggested_clean_remote_path"),
                r.get("suggested_clean_remote_path"),
                r.get("pod_id"), r.get("pod_file_path") or r.get("staged_path"),
                r.get("pod_id"), r.get("pod_file_path") or r.get("staged_path"),
                r.get("text_extraction_status"),
                r.get("pod_id"), r.get("pod_file_path") or r.get("staged_path"),
            ),
        )
        count += 1
    conn.commit()
    return count


def read_manifest_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def search_files(conn: sqlite3.Connection, query: str) -> list[sqlite3.Row]:
    q = f"%{query}%"
    cur = conn.execute(
        """
        SELECT pod_id, batch_name, filename, extension, project, category, source_path, staged_path, suggested_vault_path, copy_status, notes
        FROM files
        WHERE filename LIKE ? OR project LIKE ? OR category LIKE ? OR COALESCE(notes,'') LIKE ?
        ORDER BY COALESCE(pod_id, batch_name), filename
        """,
        (q, q, q, q),
    )
    return cur.fetchall()
