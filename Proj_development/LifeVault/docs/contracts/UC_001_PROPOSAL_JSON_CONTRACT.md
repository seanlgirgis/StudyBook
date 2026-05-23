# UC_001_PROPOSAL_JSON_CONTRACT.md

## Purpose

Defines the `proposal.json` contract for `UC_001_ingest_folder_proposal`.
This is a metadata/proposal-only artifact contract.

## Required Top-Level Fields

- `schema_version`
- `proposal_id`
- `created_at`
- `source_path`
- `source_exists`
- `scan_mode`
- `scan_status`
- `is_partial`
- `story`
- `folder_summary`
- `file_preview`
- `filename_sensitivity_summary`
- `content_scan_status`
- `content_scan_reason`
- `content_sensitivity_summary`
- `duplicate_name_summary`
- `suggested_metadata`
- `recommended_next_action`
- `allowed_next_actions`
- `forbidden_actions_in_uc_001`
- `warnings`
- `errors`

## Enums

### `scan_mode`

- `metadata_only`
- `preview_limited`

### `scan_status`

- `success`
- `partial`
- `failed`

### `content_scan_status`

- `not_performed`
- `requires_approval`
- `not_allowed_in_uc_001`

### `recommended_next_action`

- `save_only`
- `review_sensitivity_candidates`
- `ask_for_story`
- `proceed_to_uc_002`
- `proceed_to_uc_003_after_approval`
- `stop_due_to_error`

### `allowed_next_actions` (items)

- `save_only`
- `edit_proposal`
- `run_uc_002_sensitivity_scan`
- `create_pod_after_approval`
- `abandon_proposal`

### `forbidden_actions_in_uc_001` (must include)

- `copy_files`
- `write_database`
- `call_onedrive_or_rclone`
- `delete_files`
- `move_files`
- `rename_files`
- `extract_full_content`
- `write_text_cache`
- `ai_classify_full_text`

## `folder_summary` Object

Required fields:

- `file_count` (integer)
- `folder_count` (integer)
- `total_size_bytes` (integer)
- `extension_counts` (object map `{extension: count}`)
- `largest_files` (array of summary objects)
- `oldest_modified_time` (ISO-8601 string or `null`)
- `newest_modified_time` (ISO-8601 string or `null`)
- `depth_limited` (boolean)
- `max_depth_used` (integer or `null`)

## `file_preview` List

Each item must include:

- `relative_path`
- `filename`
- `extension`
- `size_bytes`
- `modified_time`
- `file_kind`
- `filename_sensitivity_level`
- `filename_sensitivity_reasons`
- `duplicate_name_group_id`
- `included_in_preview`

Constraint:

- No extracted content text is allowed in `file_preview`.

## `filename_sensitivity_summary` Object

Required fields:

- `highest_level`
- `candidate_count`
- `candidates_by_level`
- `rule_version`
- `note`

Allowed levels:

- `unknown`
- `public`
- `normal`
- `private`
- `sensitive`
- `highly_sensitive`

## Content Sensitivity Fields (UC_001 Defaults)

UC_001 must set:

- `content_scan_status = "not_performed"`
- `content_scan_reason = "UC_001 does not extract file contents by default."`
- `content_sensitivity_summary = "not_scanned"`

## `suggested_metadata` Object

Required fields:

- `suggested_pod_name`
- `suggested_project`
- `suggested_category`
- `suggested_event_name`
- `suggested_vault_path`
- `confidence`
- `reason`
- `questions_for_user`

## `warnings` / `errors` Structure

Each warning/error item:

- `code`
- `message`
- `severity`

Recommended severity values:

- `info`
- `warning`
- `error`

## Example Proposal (Fake Data)

```json
{
  "schema_version": "1.0",
  "proposal_id": "uc001_20260523_101530_fake_onboarding",
  "created_at": "2026-05-23T10:15:30Z",
  "source_path": "D:\\Intake\\FakeClient\\OnboardingPack",
  "source_exists": true,
  "scan_mode": "metadata_only",
  "scan_status": "success",
  "is_partial": false,
  "story": "Legacy onboarding documents for policy review.",
  "folder_summary": {
    "file_count": 42,
    "folder_count": 8,
    "total_size_bytes": 10485760,
    "extension_counts": {
      ".pdf": 20,
      ".docx": 12,
      ".xlsx": 10
    },
    "largest_files": [
      {
        "relative_path": "benefits/medical_overview.pdf",
        "size_bytes": 2097152
      }
    ],
    "oldest_modified_time": "2021-02-10T14:00:00Z",
    "newest_modified_time": "2026-05-01T09:30:00Z",
    "depth_limited": false,
    "max_depth_used": null
  },
  "file_preview": [
    {
      "relative_path": "hr/W4_2024.pdf",
      "filename": "W4_2024.pdf",
      "extension": ".pdf",
      "size_bytes": 120340,
      "modified_time": "2026-03-01T10:20:00Z",
      "file_kind": "document",
      "filename_sensitivity_level": "highly_sensitive",
      "filename_sensitivity_reasons": ["matched_rule:W4"],
      "duplicate_name_group_id": null,
      "included_in_preview": true
    }
  ],
  "filename_sensitivity_summary": {
    "highest_level": "highly_sensitive",
    "candidate_count": 7,
    "candidates_by_level": {
      "sensitive": 3,
      "highly_sensitive": 4
    },
    "rule_version": "filename_rules_v1",
    "note": "Filename/folder/extension signals only."
  },
  "content_scan_status": "not_performed",
  "content_scan_reason": "UC_001 does not extract file contents by default.",
  "content_sensitivity_summary": "not_scanned",
  "duplicate_name_summary": {
    "duplicate_name_candidate_count": 2,
    "groups": [
      {
        "group_id": "dup_name_001",
        "name": "onboarding_packet.pdf",
        "count": 2
      }
    ]
  },
  "suggested_metadata": {
    "suggested_pod_name": "pod_fake_onboarding_20260523",
    "suggested_project": "FakeClient",
    "suggested_category": "HR Onboarding",
    "suggested_event_name": "onboarding_packet_review",
    "suggested_vault_path": "LifeVault/01_Knowledge/HR/Onboarding",
    "confidence": 0.78,
    "reason": "Story context + dominant folder naming",
    "questions_for_user": [
      "Should payroll documents be split into a separate pod?"
    ]
  },
  "recommended_next_action": "proceed_to_uc_002",
  "allowed_next_actions": [
    "save_only",
    "edit_proposal",
    "run_uc_002_sensitivity_scan",
    "create_pod_after_approval",
    "abandon_proposal"
  ],
  "forbidden_actions_in_uc_001": [
    "copy_files",
    "write_database",
    "call_onedrive_or_rclone",
    "delete_files",
    "move_files",
    "rename_files",
    "extract_full_content",
    "write_text_cache",
    "ai_classify_full_text"
  ],
  "warnings": [
    {
      "code": "PREVIEW_LIMIT_NOT_USED",
      "message": "Full metadata scan completed.",
      "severity": "info"
    }
  ],
  "errors": []
}
```

## Validation Rules

- `proposal_id` must be unique enough for operational use and filesystem-safe.
- `source_path` may be absolute but should remain in operational artifacts, not Git-tracked outputs.
- `file_preview` must be capped for large folders.
- UC_001 artifacts must not contain extracted document text.
- Proposal artifacts must be stored outside Git repo paths.
- Contract should be testable later via Pydantic model or JSON Schema.