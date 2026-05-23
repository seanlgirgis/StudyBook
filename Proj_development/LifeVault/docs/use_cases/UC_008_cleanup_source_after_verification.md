# UC_008_cleanup_source_after_verification.md

## Goal

Allow operator-approved cleanup actions only after verified publish success.

## Safety Boundaries

- No cleanup without explicit human approval.
- Default is no delete/move/rename.

## Dependencies

UC_007 verified success, explicit cleanup policy/workflow.

## Acceptance Criteria

- Cleanup actions are gated, auditable, and reversible where possible.