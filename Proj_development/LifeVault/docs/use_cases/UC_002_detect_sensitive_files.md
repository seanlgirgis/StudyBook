# UC_002_detect_sensitive_files.md

## Goal

Flag potentially sensitive files from proposal/pod metadata for human review.

## Safety Boundaries

- No auto-delete, move, or publish.
- No OneDrive upload.

## Dependencies

UC_001 output, sensitivity policy, review UI/CLI.

## Acceptance Criteria

- Produces sensitivity candidate list with reasons.
- Supports human override decisions.