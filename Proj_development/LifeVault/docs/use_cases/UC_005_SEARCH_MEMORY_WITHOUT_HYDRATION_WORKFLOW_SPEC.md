# UC_005_SEARCH_MEMORY_WITHOUT_HYDRATION_WORKFLOW_SPEC.md

## 1. Purpose

Search indexed LifeVault metadata from SQLite without hydrating, opening, or extracting content from files.

## 2. Inputs

- query text
- optional db path
- optional filters:
  - pod_id
  - filename contains
  - extension
  - sensitivity_level
  - review_decision
  - vault_publish_status
  - project
  - category
  - event_name
  - duplicate candidates only
  - limit

## 3. Outputs

Human-readable rows including:

- file_id
- filename
- extension
- sensitivity_level
- pod_id
- pod_relative_path
- source_path or source_relative_path
- review_decision
- vault_publish_status
- duplicate_group_id (if any)

## 4. Search Types v0

Supported:

- filename substring search
- pod/story/project/category/event metadata search
- sensitivity filter
- review status filter
- duplicate candidate filter
- list all indexed pods
- list files in one pod

Not supported in v0:

- full-text document content search

## 5. What UC_005 Must Not Do

- no file content read
- no PDF parsing
- no OCR
- no text extraction
- no vector search
- no OneDrive
- no vault publish
- no source cleanup
- no DB writes

## 6. Relationship to Future Use Cases

- UC_011 handles content-based sensitivity later.
- Future FTS/text search requires approved text extraction policy.
- UC_006 publishes approved files to vault later.

## 7. Safety Model

- Use read-only SQLite connection (`mode=ro`) where practical.
- Execute only parameterized `SELECT` queries.
- No mutating SQL statements.

## 8. CLI Examples

- `python -m lifevault.uc005_cli --db-path "<db>" --query "W4"`
- `python -m lifevault.uc005_cli --db-path "<db>" --sensitivity highly_sensitive`
- `python -m lifevault.uc005_cli --db-path "<db>" --pod-id "<pod_id>"`
- `python -m lifevault.uc005_cli --db-path "<db>" --duplicates-only`
- `python -m lifevault.uc005_cli --db-path "<db>" --list-pods`