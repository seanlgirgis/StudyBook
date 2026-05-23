from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Dict, List

MIGRATION_ID = "0001_lifevault_core_schema"

EXPECTED_TABLES = [
    "schema_migrations",
    "sources",
    "pods",
    "files",
    "file_instances",
    "vault_locations",
    "tags",
    "file_tags",
    "review_decisions",
    "duplicate_groups",
    "duplicate_group_members",
    "audit_log",
    "text_cache_index",
    "export_snapshots",
]

EXPECTED_INDEXES = [
    "idx_sources_type",
    "idx_pods_status",
    "idx_pods_event_name",
    "idx_files_sha256",
    "idx_files_filename",
    "idx_files_sensitivity",
    "idx_file_instances_file_id",
    "idx_file_instances_source_id",
    "idx_file_instances_path",
    "idx_vault_locations_file_id",
    "idx_tags_name",
    "idx_file_tags_file_id",
    "idx_review_decisions_file_id",
    "idx_duplicate_members_group_id",
    "idx_audit_log_created_at",
    "idx_text_cache_file_id",
    "idx_export_snapshots_created_at",
]

CREATE_TABLE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS schema_migrations (
      version INTEGER PRIMARY KEY,
      migration_id TEXT NOT NULL UNIQUE,
      applied_at TEXT NOT NULL,
      checksum TEXT,
      notes TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sources (
      source_id TEXT PRIMARY KEY,
      source_type TEXT NOT NULL CHECK (source_type IN (
        'local_folder','onedrive_dirty','onedrive_clean','external_drive','code_repo','export','other'
      )),
      source_name TEXT NOT NULL,
      root_ref TEXT,
      remote_name TEXT,
      description TEXT,
      is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(source_type, source_name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pods (
      pod_id TEXT PRIMARY KEY,
      source_id TEXT NOT NULL,
      pod_name TEXT NOT NULL,
      event_name TEXT,
      pod_status TEXT NOT NULL CHECK (pod_status IN (
        'proposed','onboarded_needs_review','reviewed','archived','error'
      )),
      story_context TEXT,
      intake_notes TEXT,
      sensitivity_level TEXT NOT NULL DEFAULT 'unknown' CHECK (sensitivity_level IN (
        'unknown','public','normal','private','sensitive','highly_sensitive'
      )),
      storage_temperature TEXT NOT NULL DEFAULT 'unknown' CHECK (storage_temperature IN (
        'unknown','hot','warm','cold'
      )),
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(source_id, pod_name),
      FOREIGN KEY(source_id) REFERENCES sources(source_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS files (
      file_id TEXT PRIMARY KEY,
      sha256 TEXT NOT NULL,
      hash_algo TEXT NOT NULL DEFAULT 'sha256',
      filename TEXT,
      ext TEXT,
      size_bytes INTEGER,
      mime_type TEXT,
      file_status TEXT NOT NULL DEFAULT 'observed' CHECK (file_status IN (
        'observed','copied_to_pod','needs_review','approved','skipped','duplicate_candidate','published','error'
      )),
      review_status TEXT NOT NULL DEFAULT 'needs_review' CHECK (review_status IN (
        'needs_review','approved','skipped','duplicate_review','sensitive_review','archive'
      )),
      publish_status TEXT NOT NULL DEFAULT 'not_published' CHECK (publish_status IN (
        'not_published','publish_approved','published','verified','failed'
      )),
      sensitivity_level TEXT NOT NULL DEFAULT 'unknown' CHECK (sensitivity_level IN (
        'unknown','public','normal','private','sensitive','highly_sensitive'
      )),
      storage_temperature TEXT NOT NULL DEFAULT 'unknown' CHECK (storage_temperature IN (
        'unknown','hot','warm','cold'
      )),
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(sha256, hash_algo)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS file_instances (
      instance_id TEXT PRIMARY KEY,
      file_id TEXT NOT NULL,
      source_id TEXT,
      pod_id TEXT,
      instance_role TEXT NOT NULL,
      instance_path TEXT NOT NULL,
      path_is_absolute INTEGER NOT NULL DEFAULT 0 CHECK (path_is_absolute IN (0,1)),
      path_platform TEXT,
      observed_at TEXT,
      is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(file_id, instance_path, instance_role),
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
      FOREIGN KEY(source_id) REFERENCES sources(source_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
      FOREIGN KEY(pod_id) REFERENCES pods(pod_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS vault_locations (
      vault_location_id TEXT PRIMARY KEY,
      file_id TEXT NOT NULL,
      vault_path TEXT NOT NULL,
      publish_status TEXT NOT NULL CHECK (publish_status IN (
        'not_published','publish_approved','published','verified','failed'
      )),
      approved_by TEXT,
      approved_at TEXT,
      publish_batch_id TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(file_id, vault_path),
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tags (
      tag_id TEXT PRIMARY KEY,
      tag_name TEXT NOT NULL UNIQUE,
      tag_group TEXT,
      description TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS file_tags (
      file_id TEXT NOT NULL,
      tag_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      assigned_by TEXT,
      PRIMARY KEY(file_id, tag_id),
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
      FOREIGN KEY(tag_id) REFERENCES tags(tag_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS review_decisions (
      decision_id TEXT PRIMARY KEY,
      file_id TEXT NOT NULL,
      decision_type TEXT NOT NULL,
      review_status TEXT NOT NULL CHECK (review_status IN (
        'needs_review','approved','skipped','duplicate_review','sensitive_review','archive'
      )),
      publish_status TEXT NOT NULL CHECK (publish_status IN (
        'not_published','publish_approved','published','verified','failed'
      )),
      decided_by TEXT,
      decision_note TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT,
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS duplicate_groups (
      duplicate_group_id TEXT PRIMARY KEY,
      group_method TEXT NOT NULL,
      group_status TEXT NOT NULL,
      confidence_score REAL,
      note TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS duplicate_group_members (
      duplicate_group_id TEXT NOT NULL,
      file_id TEXT NOT NULL,
      member_role TEXT,
      is_canonical_candidate INTEGER NOT NULL DEFAULT 0 CHECK (is_canonical_candidate IN (0,1)),
      created_at TEXT NOT NULL,
      PRIMARY KEY(duplicate_group_id, file_id),
      FOREIGN KEY(duplicate_group_id) REFERENCES duplicate_groups(duplicate_group_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS audit_log (
      audit_id TEXT PRIMARY KEY,
      event_type TEXT NOT NULL,
      event_time TEXT NOT NULL,
      actor TEXT,
      target_table TEXT,
      target_id TEXT,
      event_status TEXT,
      event_payload_json TEXT,
      created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS text_cache_index (
      text_index_id TEXT PRIMARY KEY,
      file_id TEXT NOT NULL,
      cache_ref TEXT,
      extract_status TEXT NOT NULL,
      extract_engine TEXT,
      last_extracted_at TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(file_id, cache_ref),
      FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS export_snapshots (
      export_id TEXT PRIMARY KEY,
      export_type TEXT NOT NULL,
      artifact_path TEXT NOT NULL,
      checksum_sha256 TEXT,
      row_count INTEGER,
      trigger_reason TEXT,
      export_time TEXT NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT,
      UNIQUE(export_type, artifact_path)
    )
    """,
]

CREATE_INDEX_STATEMENTS = [
    "CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type)",
    "CREATE INDEX IF NOT EXISTS idx_pods_status ON pods(pod_status)",
    "CREATE INDEX IF NOT EXISTS idx_pods_event_name ON pods(event_name)",
    "CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256)",
    "CREATE INDEX IF NOT EXISTS idx_files_filename ON files(filename)",
    "CREATE INDEX IF NOT EXISTS idx_files_sensitivity ON files(sensitivity_level)",
    "CREATE INDEX IF NOT EXISTS idx_file_instances_file_id ON file_instances(file_id)",
    "CREATE INDEX IF NOT EXISTS idx_file_instances_source_id ON file_instances(source_id)",
    "CREATE INDEX IF NOT EXISTS idx_file_instances_path ON file_instances(instance_path)",
    "CREATE INDEX IF NOT EXISTS idx_vault_locations_file_id ON vault_locations(file_id)",
    "CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(tag_name)",
    "CREATE INDEX IF NOT EXISTS idx_file_tags_file_id ON file_tags(file_id)",
    "CREATE INDEX IF NOT EXISTS idx_review_decisions_file_id ON review_decisions(file_id)",
    "CREATE INDEX IF NOT EXISTS idx_duplicate_members_group_id ON duplicate_group_members(duplicate_group_id)",
    "CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at)",
    "CREATE INDEX IF NOT EXISTS idx_text_cache_file_id ON text_cache_index(file_id)",
    "CREATE INDEX IF NOT EXISTS idx_export_snapshots_created_at ON export_snapshots(created_at)",
]


def _enable_foreign_keys(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")


def _migration_exists(conn: sqlite3.Connection) -> bool:
    conn.execute(CREATE_TABLE_STATEMENTS[0])
    row = conn.execute(
        "SELECT 1 FROM schema_migrations WHERE migration_id = ?", (MIGRATION_ID,)
    ).fetchone()
    return row is not None


def apply_schema_v0(conn: sqlite3.Connection) -> Dict[str, object]:
    _enable_foreign_keys(conn)

    if _migration_exists(conn):
        validation = validate_schema_v0(conn)
        return {"applied": False, "already_applied": True, "validation": validation}

    applied_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    try:
        conn.execute("BEGIN")
        for stmt in CREATE_TABLE_STATEMENTS:
            conn.execute(stmt)
        for stmt in CREATE_INDEX_STATEMENTS:
            conn.execute(stmt)
        conn.execute(
            """
            INSERT INTO schema_migrations(version, migration_id, applied_at, checksum, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (1, MIGRATION_ID, applied_at, None, "Initial v0 core schema"),
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise

    validation = validate_schema_v0(conn)
    return {"applied": True, "already_applied": False, "validation": validation}


def validate_schema_v0(conn: sqlite3.Connection) -> Dict[str, object]:
    _enable_foreign_keys(conn)

    table_rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    found_tables = {r[0] for r in table_rows}

    index_rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()
    found_indexes = {r[0] for r in index_rows}

    missing_tables: List[str] = [t for t in EXPECTED_TABLES if t not in found_tables]
    missing_indexes: List[str] = [i for i in EXPECTED_INDEXES if i not in found_indexes]

    migration_row = conn.execute(
        "SELECT migration_id FROM schema_migrations WHERE migration_id = ?", (MIGRATION_ID,)
    ).fetchone()
    migration_present = migration_row is not None

    fk_issues = conn.execute("PRAGMA foreign_key_check").fetchall()
    fk_ok = len(fk_issues) == 0

    ok = not missing_tables and not missing_indexes and migration_present and fk_ok

    return {
        "ok": ok,
        "missing_tables": missing_tables,
        "missing_indexes": missing_indexes,
        "migration_present": migration_present,
        "foreign_key_issues": fk_issues,
    }