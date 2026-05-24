# UC_009 Cleanup Source After Verification Workflow Spec

## Purpose

UC_009 performs controlled post-verification cleanup by quarantining selected source file instances after UC_007 publish and UC_008 verification evidence exist.

v0 policy: cleanup is quarantine/archive only. No permanent delete.

Suggested quarantine root:

- `D:\AI_Lab\LifeVault\cleanup_quarantine`

## Inputs

- `PodId`
- `DbPath`
- `QuarantineRoot`
- `DryRun`
- `ApprovedCleanup`
- `RealDbConfirm`
- `IncludeSensitive` (optional, default `false`)

## Candidate Rules

A file instance is eligible only when all conditions hold:

1. Decision is one of:
   - `duplicate_skip`
   - `skip`
   - `archive`
2. Required related publish/verify evidence exists when relevant.
3. Operator provides explicit cleanup approval.

## Duplicate Behavior

For `duplicate_skip`:

- Quarantine only the skipped duplicate instance.
- Do not touch `duplicate_keep` instance.
- Do not touch verified vault copy.

## Safety Rules

- Dry-run writes nothing and moves nothing.
- Any move requires `ApprovedCleanup`.
- Real DB requires `RealDbConfirm`.
- Refuse cleanup when required verification is missing.
- Refuse overwrite in quarantine destination.
- No permanent delete in v0.
- No OneDrive/rclone.
- No whole-folder cleanup.
- No broad source-root cleanup.
- No `sensitive`/`highly_sensitive` cleanup unless `IncludeSensitive` is explicitly enabled.

## Outputs

- Cleanup candidate report.
- Cleanup manifest:
  - `<quarantine_root>\<pod_id>\_cleanup_manifest.csv`
- Quarantined files under:
  - `<quarantine_root>\<pod_id>\`
- `audit_log` event.

## Relationship to UC_008

- UC_008 verification is a hard prerequisite.
- UC_009 remains blocked until verification passes and evidence is available.

## Test Plan (Future Implementation)

Future implementation tests must use `tmp_path` only:

- Dry-run moves nothing.
- Approved cleanup moves only `duplicate_skip` candidate when eligible.
- Verified keep item is not moved.
- `needs_review` is not moved.
- `sensitive`/`highly_sensitive` blocked unless `IncludeSensitive`.
- Missing verification blocks cleanup.
- Overwrite refused.
- Cleanup manifest created.
- `audit_log` written.
- No real `D:\AI_Lab` paths touched.

## Implementation Reference (v0)

- `src/lifevault/uc009_cleanup_quarantine.py`
- `src/lifevault/uc009_cli.py`
- `scripts/run_uc009_cleanup_quarantine.ps1`
- `tests/test_uc009_cleanup_quarantine.py`

Current implementation status: temp-only validated in automated tests using `tmp_path`.
