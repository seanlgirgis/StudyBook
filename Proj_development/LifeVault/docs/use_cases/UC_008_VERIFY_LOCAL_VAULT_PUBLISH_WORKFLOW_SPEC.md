# UC_008 Verify Local Vault Publish Workflow Spec

## Purpose

Verify that UC_007-published local vault files match onboarding pod source copies before any cleanup workflow can be considered.

## Inputs

- `PodId`
- `DbPath`
- `VaultRoot`
- `DryRun`
- `ApprovedVerify`
- `RealDbConfirm`

## Required Artifacts

- UC_007 publish manifest:
  - `<vault_root>\<pod_id>\_publish_manifest.csv`

## Verification Steps

For each manifest row with `copy_status=copied`:

1. Confirm `source_path` exists.
2. Confirm `destination_path` exists.
3. Compare source/destination byte size.
4. Compare source/destination SHA256.

## Outputs

- Verification report:
  - `<vault_root>\<pod_id>\_verify_manifest.csv`
- Dry-run summary (no writes).
- Approved verify DB updates for matched items only.
- `audit_log` verification event.

## Rules

- Dry-run validates and reports only; no DB writes.
- Approved verify updates DB publish status to `verified` only after size/hash match.
- Real DB requires `RealDbConfirm`.
- Verification applies only to items already published via UC_007 manifest.
- Any mismatch/missing path must be marked failed and must not be marked verified.

## Safety

- No delete/move/rename.
- No source cleanup.
- No OneDrive/rclone.
- No encryption/decryption.
- No content extraction.

## Relationship to Cleanup

- UC_009 cleanup remains blocked until UC_008 verification succeeds.
- Verification success is a prerequisite, not cleanup itself.

## Test Plan

Temp-only tests (`tmp_path`) must verify:

- dry-run no DB changes
- approved verify marks matching file verified
- size mismatch fails verification
- hash mismatch fails verification
- missing destination fails safely
- missing source fails safely
- verify manifest created
- audit_log written
- no cleanup/delete/move
- no OneDrive/rclone
