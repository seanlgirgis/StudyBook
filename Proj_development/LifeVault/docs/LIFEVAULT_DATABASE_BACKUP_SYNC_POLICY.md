# LIFEVAULT_DATABASE_BACKUP_SYNC_POLICY.md

## Scope

This policy defines LifeVault operational database location, backup model, sync constraints, restore model, and agent responsibilities.

Schema design reference:

- `docs/LIFEVAULT_SCHEMA_V0_PLAN.md`
- `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`

## 1. Primary Database Name and Location

Main operational DB:

- `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

Purpose coverage:

- Searchable map
- File metadata
- Pod records
- Stories/context
- Vault locations
- Review status
- Publish status
- Duplicate status
- Sensitivity
- Hot/warm/cold status
- Audit log

## 2. Future Database/Index Names

- Keep FTS inside `lifevault.sqlite` first.
- Future semantic index candidate:
  - `D:\AI_Lab\LifeVault\vectors\lifevault_vectors.sqlite`
  - Or another documented vector store selected later.
- Vector search is not implemented in this phase.

## 3. Backup Locations

- Local DB backups: `D:\AI_Lab\LifeVault\db_backups`
- Export artifacts: `D:\AI_Lab\LifeVault\exports`
- Future private vault backup target:
  - `onedrive_clean:LifeVault/99_System_Exports/LifeVault_Admin/`

## 4. Backup File Naming

Timestamped naming standard:

- `lifevault_YYYYMMDD_HHMMSS.sqlite`
- `lifevault_YYYYMMDD_HHMMSS.sqlite.sha256`
- `lifevault_snapshot_YYYYMMDD_HHMMSS.json`
- `lifevault_files_YYYYMMDD_HHMMSS.csv`
- `lifevault_pods_YYYYMMDD_HHMMSS.csv`
- `lifevault_audit_YYYYMMDD_HHMMSS.csv`

## 5. Backup Method

Policy requirements:

- Do not casually copy a live SQLite DB as the main backup method.
- Use SQLite backup API (`sqlite3 backup`) in backup scripts.
- Write checksum files for backup artifacts.
- Verify backup readability before marking success.
- Log success/failure of backup jobs.
- If WAL mode is introduced later, handle WAL/checkpoint behavior safely.

## 6. Sync Model

v0 sync rule:

- One writer machine
- Many reader/search machines

Initial writer machine:

- ASUS PC

Constraints:

- Do not sync the live DB for simultaneous writes.
- Syncable/private artifacts:
  - Timestamped DB backups
  - JSON/CSV exports
  - Recovery notes

Not public Git:

- Real `lifevault.sqlite`
- DB backups
- Exports with real filenames/stories
- Text cache
- Pod manifests
- Reports
- Logs
- Secrets/tokens

## 7. Portability/Restore Model

To operate on another machine:

1. Clone/pull LifeVault repo.
2. Configure machine-local `config/paths.local.json`.
3. Configure and verify rclone remotes.
4. Restore DB backup or import snapshot.
5. Start in reader/search mode.
6. Promote to writer mode intentionally.

## 8. Protection/Encryption

Phase 1:

- Keep private operational folder outside Git.
- Keep real DB/exports out of public Git.

Phase 2 (future required work):

- Encrypted DB backup archives.
- Encrypted sensitive exports.
- Possible separate sensitive DB or encrypted zone.

Encryption is not implemented in this phase and must be designed before sensitive text extraction workflows.

## 9. Agent Responsibilities

ChatGPT responsibilities:

- Distinguish repository, operational data, operational DB, and clean vault.
- Do not suggest committing real DB/exports to Git.
- Recommend backup before risky operations.
- Keep one-writer/many-reader model explicit.

Codex responsibilities:

- Do not casually copy/sync live DB to cloud.
- Do not commit DB/backups/exports/logs.
- Use backup scripts once implemented.
- Report DB files touched.
- Do not invent multi-machine simultaneous write workflows.

## 10. Implementation Status in This Bite

- Documentation only.
- No backup scripts created.
- No operational DB created or modified.
- No real files processed.
- No OneDrive upload.
