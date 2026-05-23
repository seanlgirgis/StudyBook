# UC_003_CREATE_ONBOARDING_POD_WORKFLOW_SPEC.md

## Scope

Design/spec for UC_003 pod creation workflow.
This is specification-only and does not execute copy operations.

Contract reference:

- `docs/contracts/UC_003_POD_PROFILE_AND_MANIFEST_CONTRACT.md`

Implementation references:

- `src/lifevault/uc003_pod.py`
- `src/lifevault/uc003_cli.py`
- `scripts/run_uc003_create_pod.ps1`

## Purpose

Given an accepted UC_001 proposal package and explicit human approval, create a controlled onboarding pod under:

- `D:\AI_Lab\LifeVault\onboarding\pods\<pod_id>\`

Source folder remains untouched.

Policy note:

- User-facing "move to store" is a future workflow, but internally it must be decomposed as:
  1. copy to controlled destination
  2. verify copy
  3. record status/audit trail
  4. explicit human approval
  5. cleanup/removal in a separate later use case

## 1. Inputs

- `proposal_id` or `proposal_path`
- explicit `approval` flag
- optional approved pod name
- optional approved story
- optional approved project/category/event fields
- optional include/exclude decisions (future)

## 2. Preconditions

- UC_001 proposal exists.
- Proposal `scan_status` is `success` or accepted `partial`.
- `source_path` still exists and is readable.
- Human approval is explicit.
- Operational pod root exists.
- No database write required.
- No OneDrive/rclone required.

## 3. Output Pod Structure

`D:\AI_Lab\LifeVault\onboarding\pods\<pod_id>\`

- `original_copies\`
- `reports\`
- `_pod_profile.json`
- `_pod_manifest.csv`
- `_review.csv`
- `_notes.md`
- `_source_proposal_snapshot.json`

## 4. Copy Behavior

- Copy only.
- Preserve original filenames.
- Preserve relative folder structure when nested.
- Do not delete source.
- Do not move source.
- Do not rename source.
- Do not modify source.
- Do not upload to OneDrive.
- Do not sync.
- Do not extract contents.
- Do not write text cache.
- Do not perform source free-space operations in UC_003.
- Do not treat pod as final source of truth.

## 5. Pod Profile Fields

Required fields:

- `pod_id`
- `created_at`
- `source_path`
- `source_proposal_id`
- `story`
- `project`
- `category`
- `event_name`
- `suggested_vault_path`
- `pod_status`
- `sensitivity_highest_level`
- `file_count`
- `copied_file_count`
- `duplicate_candidate_count`
- `notes`

## 6. Pod Manifest Fields

Required fields:

- `pod_id`
- `source_relative_path`
- `source_absolute_path`
- `pod_relative_path`
- `pod_absolute_path`
- `filename`
- `extension`
- `size_bytes`
- `modified_time`
- `copied_at`
- `filename_sensitivity_level`
- `filename_sensitivity_reasons`
- `duplicate_name_group_id`
- `copy_status`
- `copy_error`

## 7. Review CSV Fields

Initial review file fields:

- `pod_id`
- `pod_relative_path`
- `filename`
- `suggested_sensitivity_level`
- `user_sensitivity_level`
- `review_decision`
- `user_notes`
- `approved_for_database_index`
- `approved_for_vault_publish`

Defaults:

- `review_decision = needs_review`
- `approved_for_database_index = false`
- `approved_for_vault_publish = false`

## 8. Safety Checks

Before copy:

- Verify proposal path is outside Git repo.
- Verify pod output path is outside Git repo.
- Verify source path is not inside pod output path.
- Verify source path exists.
- Verify destination pod path does not already exist.
- Verify approval flag is present.
- Refuse path traversal in relative paths.
- Refuse to overwrite existing pod files.

## 9. Failure Behavior

- If one file copy fails, record error in manifest.
- No delete/move rollback from source.
- Set pod status to `error` or `partial_copy`.
- User review required before retry.
- Do not silently continue without report.

## 10. Relationship to UC_004

- UC_003 does not write SQLite.
- UC_004 indexes accepted pod metadata into DB later.

## 11. Relationship to UC_006/UC_007/UC_008

- UC_003 does not publish to vault.
- UC_003 does not verify vault copies.
- UC_003 does not clean source files.
- These remain separate future use cases.

## 12. Acceptance Criteria

- Pod creation requires explicit approval.
- Selected files are copied only to `original_copies`.
- Source remains unchanged.
- Pod profile/manifest/review files are created.
- No DB write occurs.
- No OneDrive/rclone operation occurs.
- No deletion/move/rename occurs.
- Errors are visible and reviewable.

## 13. Test Plan (Future Implementation)

All tests must use temporary folders only.

- Create pod from fake proposal.
- Preserve filenames and relative structure.
- Source files remain unchanged.
- Manifest rows are complete and correct.
- Review defaults are `needs_review` / `false` / `false`.
- No DB is created.
- Approval required to proceed.
- Existing pod destination path is refused.
- Path traversal input is refused.
