# UC_007 Publish Approved Files to Local Vault Workflow Spec

## Purpose

UC_007 v0 publishes only `ready_to_publish` file instances by copying from onboarding pod `original_copies` into a local clean vault area.

## Scope

- Local vault copy workflow only.
- No encryption in this bite (deferred security phase).
- No OneDrive/rclone operations in this bite.

## Suggested Local Vault Root

- `D:\AI_Lab\LifeVault\vault_local`
- Or machine-configurable vault root path.

## Inputs

- `PodId`
- `DbPath`
- `VaultRoot`
- `ApprovedPublish` flag
- `DryRun` flag
- `RealDbConfirm` flag

## Outputs

- Copied files in local vault destination.
- Publish manifest (planned artifact for copy results and conflict outcomes).
- DB publish status updates for successfully copied items only.
- Audit log entry for dry-run or approved publish execution.

## Eligibility Rules

Only rows classified by UC_006B as `ready_to_publish` may be copied.

Must never publish:

- `blocked_duplicate_skip`
- `blocked_needs_review`
- `blocked_sensitive_review`
- `blocked_not_approved`
- `blocked_archive`
- `blocked_skip`

## Safety Rules

- Dry-run first.
- Real DB operations require `RealDbConfirm`.
- Write/copy requires `ApprovedPublish`.
- No source deletion, move, or rename.
- No pod cleanup.
- No OneDrive/rclone.
- No content extraction.
- No text cache writes.

## Sensitive Data Rule

- `sensitive`/`highly_sensitive` instances are publishable only if already `ready_to_publish`.
- This means explicit review decision and explicit publish approval were already recorded.

## Conflict Policy (v0)

- Refuse overwrite by default.
- If destination exists, mark manifest status as conflict/blocked.
- Future phases may add versioned naming policies.

## DB Update Rule

- Update publish status only after copy succeeds for that specific instance.
- Failed/conflicted items remain not published.

## Relationship to Other Use Cases

- UC_006B provides readiness classification.
- UC_007 performs local publish copy.
- UC_008 remains separate source cleanup workflow after verification.
- OneDrive/cloud publish remains deferred until encryption design phase.

## Test Plan (Future Implementation)

Use temp DB + temp vault only:

- Dry-run copies nothing and writes no publish status.
- Approved run copies only `ready_to_publish`.
- `duplicate_skip` and `needs_review` never copied.
- Sensitive/highly_sensitive blocked unless explicitly ready.
- Overwrite refused by default.
- No OneDrive/rclone calls.
- No source deletion/move/rename.

## Implementation Reference (v0)

- `src/lifevault/uc007_publish_local.py`
- `src/lifevault/uc007_cli.py`
- `scripts/run_uc007_publish_local.ps1`
- `tests/test_uc007_publish_local.py`

Current implementation status: temp-only validated in automated tests using `tmp_path`.
