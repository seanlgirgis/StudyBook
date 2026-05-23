# UC_001_ingest_folder_proposal.md

## Use Case ID

UC_001

## Name

Ingest Folder Proposal

## Goal

Given a source folder and optional story/context, produce a proposal package for review. UC_001 is investigation/proposal only, not ingestion.

## Input

- `SourcePath`
- optional `story/context`
- optional scan depth/preview controls (future)

## Output

Proposal package under operational proposals area:

- `D:\AI_Lab\LifeVault\onboarding\proposals\<proposal_id>\`
- `proposal.json`
- optional `summary.md`
- optional `file_preview.csv`
- optional `filename_sensitivity_candidates.csv`
- optional `duplicate_name_candidates.csv`

Contract reference:

- `docs/contracts/UC_001_PROPOSAL_JSON_CONTRACT.md`

## Primary Actor

Sean

## Supporting Actors

ChatGPT, Codex, future Streamlit control center

## Trigger

Operator requests intake assessment for a local folder.

## Preconditions

- Source path is provided.
- Proposal-only mode is confirmed.
- Config resolves operational proposals path.

## Main Success Path

1. Validate source path exists and is readable.
2. Enumerate folder/file metadata only.
3. Build metadata summary and filename/rule-based sensitivity hints.
4. Capture optional story/context.
5. Write proposal package artifacts.
6. Return recommended next action + allowed next actions.

## Alternate Paths

- Large source: run preview/depth-limited scan and mark proposal partial.
- No story provided: proceed metadata-only.

## Failure Paths

- Missing/inaccessible path: fail with actionable error and no side effects.
- Permission-limited path: produce partial proposal with explicit warning.

## Safety Rules

- No file copy.
- No DB write.
- No OneDrive/rclone operation.
- No delete/move/rename.
- No full content extraction.
- No text cache writes.
- No AI content classification from full extracted text.

## Proposal Field Requirements

- `proposal_id`
- `source_path`
- `story`
- `scan_mode`
- `content_scan_status`
- `content_scan_reason`
- `filename_sensitivity_summary`
- `content_sensitivity_summary`
- `recommended_next_action`
- `allowed_next_actions`
- `forbidden_actions_in_uc_001`

Default values:

- `scan_mode`: `metadata_only`
- `content_scan_status`: `not_performed`
- `content_scan_reason`: `UC_001 does not extract file contents by default.`
- `content_sensitivity_summary`: `not_scanned`

## Data Created/Updated

- Proposal package artifacts only.

## Database Impact

- None.

## File-System Impact

- Read-only source inspection.
- Writes only to proposal package destination.

## Git/Privacy Impact

- Proposal artifacts with real metadata must remain outside Git-tracked repo paths.

## OneDrive/Vault Impact

- None.

## Local AI Role

- Assist summary interpretation from metadata/story only.

## Codex Role

- Implement proposal generator and tests in strict metadata-only mode.
- Implementation modules:
  - `src/lifevault/uc001_proposal.py`
  - `src/lifevault/uc001_cli.py`
  - `scripts/run_uc001_proposal.ps1`

## Streamlit Role

- Future UI for selecting source and reviewing proposal package.

## Approval Gates

- Human approval required before UC_003 or UC_011 style deeper actions.

## Acceptance Criteria

- Proposal package generated from valid source path.
- No copy, no DB write, no OneDrive/rclone call.
- No content extraction or text cache output.
- Recommended next action and action guardrails are explicit.
- CLI invocation is available:
  - `python -m lifevault.uc001_cli --source-path "<folder>" --story "<story>"`

## Test Cases

- Valid source path generates proposal package.
- Missing path fails safely.
- Preview mode returns partial marker.
- Proposal JSON includes required fields + defaults.

## Out of Scope

- Pod creation.
- Database indexing.
- Content extraction/classification.
- Publishing to vault.

## v0 Clarification

- UC_001 v0 includes embedded UC_002-lite behavior:
  - metadata/filename/story-based sensitivity hints
  - duplicate-name candidate hints
- UC_001 does not perform content inspection/extraction.

## Related Use Cases

UC_002, UC_003, UC_004, UC_009, UC_011
