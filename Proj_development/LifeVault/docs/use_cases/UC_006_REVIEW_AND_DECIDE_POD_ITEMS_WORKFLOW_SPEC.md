# UC_006 Review and Decide Pod Items Workflow Spec

## 1. Purpose

UC_006 records human review decisions for indexed pod file instances in SQLite metadata, before any vault publish workflow.

## 2. Inputs

- `pod_id` (required)
- `db_path` (required)
- `--list-items` or `--list-duplicates` for read operations
- `pod_relative_path` for item update operations
- `decision` and/or `approved_for_vault_publish`
- `--approved-update` for DB writes
- `--real-db-confirm` when using `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

## 3. Outputs

- Read mode: instance-oriented review rows for the pod.
- Update mode: persisted review decision metadata in `review_decisions` and aligned `files.review_status` / `files.publish_status`.

## 4. Review Decision Values

- `needs_review`
- `keep`
- `skip`
- `duplicate_keep`
- `duplicate_skip`
- `sensitive_review`
- `archive`

## 5. Duplicate Review Behavior

- Duplicate review is instance/path-aware for operator UX.
- Exact content duplicates may share one `file_id` across multiple `file_instances`.
- UC_006 applies decisions to a specific `pod_relative_path` and records instance context in review metadata.
- No duplicate deletion happens in UC_006.

## 6. Sensitive File Review Behavior

- Sensitive items may be marked `sensitive_review`.
- UC_006 does not open content, extract text, or classify file contents.
- Any future content-based sensitivity work remains gated under UC_011.

## 7. Approval for Future Vault Publish

- UC_006 may mark per-instance review intent and publish approval metadata.
- Publish approval in UC_006 is metadata only.
- Actual vault copy/publish is deferred to UC_007+ workflows.

## 8. What UC_006 Must Not Do

- No file copy, move, delete, or rename.
- No source cleanup.
- No OneDrive/rclone operations.
- No vault publish.
- No content extraction or text cache writes.

## 9. Relationship to UC_007 Publish

- UC_006 prepares reviewed metadata and approvals.
- UC_007 will later use approved review outcomes to publish files.
- UC_007 must still enforce publish safety gates and verification steps.

## 10. Test Plan

Temp-only tests (`tmp_path`) must verify:

- list review items for a pod
- list duplicate candidates for a pod
- update `keep`, `duplicate_keep`, `duplicate_skip`
- publish approval defaults to false/not_published unless explicitly set
- write operations require `--approved-update`
- real DB requires `--real-db-confirm`
- no file operations and no OneDrive/rclone calls

## 11. UC_006B Publish Readiness Review

Read-only readiness command:

- `python -m lifevault.uc006_cli --db-path "<db>" --pod-id "<pod_id>" --publish-readiness`
- `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -PublishReadiness`

Readiness statuses:

- `ready_to_publish`
- `blocked_duplicate_skip`
- `blocked_needs_review`
- `blocked_sensitive_review`
- `blocked_not_approved`
- `blocked_archive`
- `blocked_skip`

UC_006B does not publish files. It prepares UC_007 by showing exactly which instances are ready versus blocked.
