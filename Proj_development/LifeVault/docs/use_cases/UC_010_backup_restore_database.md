# UC_010_backup_restore_database.md

## Goal

Run safe backup/restore lifecycle for LifeVault DB with validation and auditability.

## Safety Boundaries

- Backup before risky operations.
- No destructive rollback on populated DB without explicit approval.

## Dependencies

Backup/sync policy, operations runbook, migration tooling maturity.

## Acceptance Criteria

- Backup artifacts are timestamped and checksummed.
- Restore drill succeeds on reader mode before writer promotion.