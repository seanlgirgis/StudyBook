# SUPER_USE_CASE_001_LOCAL_FOLDER_LIFECYCLE.md

## Purpose

Capture the complete v0 local folder lifecycle from intake to quarantine cleanup using existing UC_001 through UC_009 workflows.

Positioning note:

This document captures the first proven vertical slice of LifeVault (`SUC_006` and enabling portions of `SUC_001`), not the complete product capability map.

## Actor

- Primary actor: Sean (human operator approval authority)
- Supporting actors: ChatGPT (planning/coordination), Codex (implementation/execution)

## Inputs

- Source folder path
- Optional story/context
- LifeVault DB path
- Operational roots (pods, vault local, quarantine)
- Explicit approval flags per stage

## Outputs

- Proposal package
- Onboarding pod
- Indexed metadata in SQLite
- Review decisions/readiness states
- Local vault published copy
- Verification manifest and DB verified status
- Quarantine cleanup manifest for approved cleanup candidates

## Operational Folders

- Source input example: `D:\Users\shareuser\Downloads\apod`
- Proposals: `D:\AI_Lab\LifeVault\onboarding\proposals`
- Pods: `D:\AI_Lab\LifeVault\onboarding\pods`
- Local vault: `D:\AI_Lab\LifeVault\vault_local`
- Quarantine: `D:\AI_Lab\LifeVault\cleanup_quarantine`

## DB Path

- `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

## End-to-End Flow (v0)

1. UC_001 folder proposal
2. UC_002-lite filename/rule sensitivity (embedded in UC_001)
3. UC_003 onboarding pod creation
4. UC_004 DB indexing
5. UC_005 metadata search without hydration
6. UC_006 review decisions
7. UC_006B publish readiness
8. UC_007 local vault publish
9. UC_008 verify local vault publish
10. UC_009 quarantine cleanup after verification

## Safety Gates

- Explicit approval required for write/move stages.
- Real DB guarded by `--real-db-confirm`.
- Dry-run-first policy for UC_004/UC_007/UC_008/UC_009.
- No OneDrive/rclone in this local lifecycle.
- No permanent delete in v0.
- Sensitive/highly_sensitive publish/cleanup requires explicit gates.

## Simple PowerShell Command Pattern

```powershell
# UC_001 proposal
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc001_proposal.ps1 -SourcePath "<source>"

# UC_003 pod creation
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc003_create_pod.ps1 -ProposalPath "<proposal.json>" -Approved

# UC_004 index pod (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod>" -DbPath "<db>" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod>" -DbPath "<db>" -Approved -RealDbConfirm

# UC_005 search
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc005_search.ps1 -PodId "<pod_id>"

# UC_006 review + readiness
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -PublishReadiness -RealDbConfirm

# UC_007 publish (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "<db>" -VaultRoot "<vault_root>" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "<db>" -VaultRoot "<vault_root>" -ApprovedPublish -RealDbConfirm

# UC_008 verify (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "<db>" -VaultRoot "<vault_root>" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "<db>" -VaultRoot "<vault_root>" -ApprovedVerify -RealDbConfirm

# UC_009 cleanup quarantine (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "<db>" -QuarantineRoot "<quarantine_root>" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "<db>" -QuarantineRoot "<quarantine_root>" -ApprovedCleanup -RealDbConfirm
```

## Acceptance Criteria

- End-to-end lifecycle produces auditable artifacts at every stage.
- Publish and cleanup are both gated and reversible-in-practice (quarantine vs delete).
- Only approved candidates are published/verified/cleaned.
- No OneDrive sync/upload performed in this v0 local lifecycle.
- `pytest` baseline remains green.

## Current Real Validation Summary

- `pod_id`: `pod_uc001_20260523_061147_apod`
- Source folder: `D:\Users\shareuser\Downloads\apod`
- DB: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
- Local vault root: `D:\AI_Lab\LifeVault\vault_local`
- Quarantine root: `D:\AI_Lab\LifeVault\cleanup_quarantine`
- Published/verified file: `Template parta cover letter_2026.pdf`
- Quarantined duplicate: `Template parta cover letter_2026 (1).pdf`
- Final automated test count: `83 passed`
- Latest git checkpoint: `ecc2e3a` (`Quick Update 2026-05-23 20:13`)

## Operational Run References

- Acceptance test plan:
  - `docs/super_use_cases/SUC_001_ACCEPTANCE_TEST_PLAN.md`
- Operator checklist:
  - `docs/super_use_cases/SUC_001_OPERATOR_CHECKLIST.md`

## Known Limitations

- Encryption/decryption not yet implemented.
- Cloud publish/sync not yet enabled.
- Duplicate model remains file-level in some tables; instance-level semantics handled in workflow logic.
- Cleanup is quarantine-only in v0.

## Future Enhancement Backlog

- Encrypted publish and secure view flows.
- OneDrive/cloud publish after encryption design approval.
- Richer duplicate-instance data model.
- Bulk lifecycle orchestration (SUC-level operator commands).
- GUI orchestration for full lifecycle checkpoints.
