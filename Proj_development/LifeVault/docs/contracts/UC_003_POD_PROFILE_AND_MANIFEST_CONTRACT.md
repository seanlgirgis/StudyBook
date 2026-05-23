# UC_003_POD_PROFILE_AND_MANIFEST_CONTRACT.md

## Scope

Strict contract for UC_003 pod outputs. This is design-only and defines deterministic artifact structure and field requirements.

## 1. Pod Folder Structure

`D:\AI_Lab\LifeVault\onboarding\pods\<pod_id>\`

- `original_copies\`
- `reports\`
- `_pod_profile.json`
- `_pod_manifest.csv`
- `_review.csv`
- `_notes.md`
- `_source_proposal_snapshot.json`

## 2. `_pod_profile.json` Contract

Required fields:

- `schema_version`
- `pod_id`
- `created_at`
- `source_path`
- `source_proposal_id`
- `source_proposal_path`
- `story`
- `project`
- `category`
- `event_name`
- `suggested_vault_path`
- `pod_status`
- `sensitivity_highest_level`
- `file_count`
- `copied_file_count`
- `failed_copy_count`
- `duplicate_candidate_count`
- `content_scan_status`
- `database_index_status`
- `vault_publish_status`
- `notes`
- `warnings`
- `errors`

## 3. `_pod_manifest.csv` Contract

Required columns:

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

## 4. `_review.csv` Contract

Required columns:

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

## 5. `_notes.md` Contract

Must include:

- pod id
- source path
- story
- created timestamp
- safety note: source files were copied only; source remains untouched
- next safe actions

## 6. `_source_proposal_snapshot.json` Contract

- Must be an exact snapshot/copy of accepted UC_001 `proposal.json` at pod creation time.

## 7. Enums

### `pod_status`

- `created`
- `partial_copy`
- `error`
- `reviewed`
- `archived`

### `copy_status`

- `copied`
- `failed`
- `skipped`

### `review_decision`

- `needs_review`
- `keep`
- `skip`
- `duplicate_review`
- `sensitive_review`
- `archive`

### `content_scan_status`

- `not_performed`
- `requires_approval`
- `not_allowed_in_uc003`

### `database_index_status`

- `not_indexed`
- `index_approved`
- `indexed`
- `failed`

### `vault_publish_status`

- `not_published`
- `publish_approved`
- `published`
- `verified`
- `failed`

## 8. Validation Rules

- `pod_id` must be filesystem-safe.
- Pod output path must be outside Git repo.
- Source proposal path must be outside Git repo.
- Source path must exist before copy.
- Destination pod path must not already exist.
- Source path must not be inside destination pod path.
- No path traversal in `source_relative_path` or `pod_relative_path`.
- Manifest row count must match `file_count` or explicitly explain failures.
- `copied_file_count + failed_copy_count` must equal `file_count`.
- No full content text stored in pod metadata artifacts.
- No DB writes in UC_003.
- No OneDrive/rclone calls in UC_003.

## 9. Example Fake Pod Profile

```json
{
  "schema_version": "1.0",
  "pod_id": "pod_uc003_20260523_103000_apod",
  "created_at": "2026-05-23T10:30:00Z",
  "source_path": "D:\\Intake\\FakeFolder\\apod",
  "source_proposal_id": "uc001_20260523_061147_apod",
  "source_proposal_path": "D:\\AI_Lab\\LifeVault\\onboarding\\proposals\\uc001_20260523_061147_apod\\proposal.json",
  "story": "Fake onboarding packet for contract example",
  "project": "FakeProject",
  "category": "Onboarding",
  "event_name": "apod_intake",
  "suggested_vault_path": "LifeVault/01_Knowledge/HR/Onboarding",
  "pod_status": "created",
  "sensitivity_highest_level": "highly_sensitive",
  "file_count": 3,
  "copied_file_count": 3,
  "failed_copy_count": 0,
  "duplicate_candidate_count": 1,
  "content_scan_status": "not_performed",
  "database_index_status": "not_indexed",
  "vault_publish_status": "not_published",
  "notes": "Initial pod created from accepted proposal",
  "warnings": [],
  "errors": []
}
```

## 10. Example Fake Manifest Rows

```csv
pod_id,source_relative_path,source_absolute_path,pod_relative_path,pod_absolute_path,filename,extension,size_bytes,modified_time,copied_at,filename_sensitivity_level,filename_sensitivity_reasons,duplicate_name_group_id,copy_status,copy_error
pod_uc003_20260523_103000_apod,forms/W4.pdf,D:\Intake\FakeFolder\apod\forms\W4.pdf,original_copies/forms/W4.pdf,D:\AI_Lab\LifeVault\onboarding\pods\pod_uc003_20260523_103000_apod\original_copies\forms\W4.pdf,W4.pdf,.pdf,120000,2026-05-20T14:00:00Z,2026-05-23T10:31:00Z,highly_sensitive,matched:w4,,copied,
pod_uc003_20260523_103000_apod,forms/cover_letter.pdf,D:\Intake\FakeFolder\apod\forms\cover_letter.pdf,original_copies/forms/cover_letter.pdf,D:\AI_Lab\LifeVault\onboarding\pods\pod_uc003_20260523_103000_apod\original_copies\forms\cover_letter.pdf,cover_letter.pdf,.pdf,90000,2026-05-18T09:00:00Z,2026-05-23T10:31:01Z,normal,no_sensitive_rule_match,dup_name_001,copied,
pod_uc003_20260523_103000_apod,forms/cover_letter (1).pdf,D:\Intake\FakeFolder\apod\forms\cover_letter (1).pdf,original_copies/forms/cover_letter (1).pdf,D:\AI_Lab\LifeVault\onboarding\pods\pod_uc003_20260523_103000_apod\original_copies\forms\cover_letter (1).pdf,cover_letter (1).pdf,.pdf,91000,2026-05-18T09:00:05Z,2026-05-23T10:31:02Z,normal,no_sensitive_rule_match,dup_name_001,copied,
```

## 11. Example Fake Review Rows

```csv
pod_id,pod_relative_path,filename,suggested_sensitivity_level,user_sensitivity_level,review_decision,user_notes,approved_for_database_index,approved_for_vault_publish
pod_uc003_20260523_103000_apod,original_copies/forms/W4.pdf,W4.pdf,highly_sensitive,,needs_review,,false,false
pod_uc003_20260523_103000_apod,original_copies/forms/cover_letter.pdf,cover_letter.pdf,normal,,needs_review,,false,false
pod_uc003_20260523_103000_apod,original_copies/forms/cover_letter (1).pdf,cover_letter (1).pdf,normal,,needs_review,,false,false
```

## 12. Acceptance Criteria

UC_003 implementation is not accepted unless:

- All contract files are created.
- Source files remain untouched.
- Copy-only behavior is proven in temp tests.
- Manifest/review/profile match this contract.
- No DB is created or modified.
- No OneDrive/rclone call is made.
- No delete/move/rename/sync behavior occurs.