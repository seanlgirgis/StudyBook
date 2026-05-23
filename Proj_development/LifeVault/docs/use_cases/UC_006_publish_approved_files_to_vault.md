# UC_006_publish_approved_files_to_vault.md

## Goal

Publish only approved files to clean vault via controlled workflow.

## Safety Boundaries

- Explicit approval gate required.
- Publish only from approved queue.

## Dependencies

UC_004, UC_007 readiness checks, publish policy.

## Acceptance Criteria

- Only approved files are published.
- Publish state and audit events recorded.