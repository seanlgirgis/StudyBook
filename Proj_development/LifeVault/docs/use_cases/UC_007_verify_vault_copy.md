# UC_007_verify_vault_copy.md

## Goal

Verify published vault copies by path/hash/status consistency checks.

## Safety Boundaries

- Verification first, no cleanup side effects.

## Dependencies

UC_006 output, hash/check tooling.

## Acceptance Criteria

- Verification report marks success/failure per published item.
- Failed verification blocks downstream cleanup.