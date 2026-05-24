# UC_006_publish_approved_files_to_vault.md

## Status

Deprecated as active UC_006 scope.
Publishing is now planned under UC_007.
Active UC_006 definition:
- `docs/use_cases/UC_006_REVIEW_AND_DECIDE_POD_ITEMS_WORKFLOW_SPEC.md`
- includes UC_006B read-only publish readiness review before UC_007
Encryption/cloud publish are deferred security phases:
- `docs/security/LIFEVAULT_SECURITY_BACKLOG.md`

## Goal

Historical placeholder. Do not use as current UC_006 workflow.
For active publish planning use:
- `docs/use_cases/UC_007_PUBLISH_APPROVED_FILES_TO_LOCAL_VAULT_WORKFLOW_SPEC.md`

## Safety Boundaries

- Explicit approval gate required.
- Publish only from approved queue.

## Dependencies

UC_004, UC_007 readiness checks, publish policy.

## Acceptance Criteria

- Only approved files are published.
- Publish state and audit events recorded.
