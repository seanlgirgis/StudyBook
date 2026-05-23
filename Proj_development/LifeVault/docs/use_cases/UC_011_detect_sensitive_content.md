# UC_011_detect_sensitive_content.md

## Use Case ID

UC_011

## Name

Detect Sensitive Content (Gated Future)

## Goal

Perform content-based sensitivity detection for approved files or approved pods under explicit human approval.

## Approval Requirement

- Explicit human approval is mandatory before opening/extracting file content.

## Content Scan Modes

- `preview_only`
- `limited_text`
- `full_text`
- `ocr_later`

## Safety and Privacy Rules

- Redaction rules required for findings/reports.
- No extracted sensitive text in console logs.
- No extracted sensitive text in Git.
- No extracted sensitive text in normal logs.
- Text cache use requires approved storage policy.
- Local/private model preferred when AI classification is used.
- AI suggestions are advisory only, not source of truth.
- `highly_sensitive` files default to extraction disabled until explicitly approved.

## Outputs

- `content_sensitivity_candidates.csv`
- redacted findings
- extraction status
- future `text_cache_index` references
- recommended review actions

## Must Not Do

- Must not publish to vault.
- Must not delete/move/rename source files.
- Must not run cleanup actions.
- Must not expose full sensitive text in reports.

## Dependencies

UC_002 outcomes, approval workflow, storage/privacy policy, backup policy.

## Acceptance Criteria

- Runs only after explicit approval.
- Produces redacted findings with extraction status.
- Keeps sensitive text out of logs/Git/reports.