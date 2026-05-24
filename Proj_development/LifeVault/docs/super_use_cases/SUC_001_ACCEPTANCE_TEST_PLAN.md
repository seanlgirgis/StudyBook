# SUC_001_ACCEPTANCE_TEST_PLAN.md

## Purpose

Provide a repeatable acceptance test for `SUC_001 Local Folder Lifecycle` so the full v0 product workflow can be rerun safely and assessed consistently.

## Prerequisites

1. Repository is current and tests pass.
2. Environment initialized with:
   - `..\..\env_setter.ps1`
3. Real DB is initialized and backed up.
4. Operator has explicit approval authority for write stages.
5. One writer machine is active.

## Safe Test Folder Requirements

- Use a controlled local folder (not system roots, not OneDrive live sync roots).
- Prefer a copied/frozen test set for repeatability.
- Source folder must remain accessible for verify/cleanup gates.
- Do not use folders containing unmanaged secrets unless explicitly intended.

## Backup Requirement Before DB Writes

Before UC_004/UC_006/UC_007/UC_008/UC_009 approved actions:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\backup_lifevault_db.ps1
```

## Command Sequence (Simple PowerShell)

```powershell
# 1) UC_001 Proposal
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc001_proposal.ps1 -SourcePath "<source_path>" -Story "<story_optional>"

# 2) UC_003 Pod Creation
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc003_create_pod.ps1 -ProposalPath "<proposal_json>" -Approved

# 3) UC_004 Index (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod_path>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod_path>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -Approved -RealDbConfirm

# 4) UC_005 Search
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc005_search.ps1 -PodId "<pod_id>"

# 5) UC_006 Decisions + UC_006B Readiness
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -ListItems -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -PublishReadiness -RealDbConfirm

# 6) UC_007 Publish (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -ApprovedPublish -RealDbConfirm

# 7) UC_008 Verify (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -ApprovedVerify -RealDbConfirm

# 8) UC_009 Cleanup Quarantine (dry-run then approved)
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -QuarantineRoot "D:\AI_Lab\LifeVault\cleanup_quarantine" -DryRun -RealDbConfirm
powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -QuarantineRoot "D:\AI_Lab\LifeVault\cleanup_quarantine" -ApprovedCleanup -RealDbConfirm
```

## Expected Outputs By Stage

1. UC_001: proposal package in `onboarding\proposals\...`
2. UC_003: pod structure in `onboarding\pods\<pod_id>\...`
3. UC_004: pod metadata in DB + audit event
4. UC_005: searchable metadata rows for pod/items
5. UC_006/006B: review decisions and readiness breakdown
6. UC_007: local vault copy + `_publish_manifest.csv`
7. UC_008: `_verify_manifest.csv` + verified DB statuses for matched items
8. UC_009: quarantine moves + `_cleanup_manifest.csv`

## Pass / Fail Criteria

Pass:

- Every dry-run succeeds with zero writes/moves.
- Approved stages operate only on eligible records.
- UC_007 publishes only `ready_to_publish`.
- UC_008 verifies published files successfully where expected.
- UC_009 quarantines only eligible cleanup candidates.
- No permanent delete occurs.

Fail:

- Any stage performs actions outside eligibility/safety gates.
- Missing manifests/audit records for approved actions.
- Sensitive/highly_sensitive handling bypasses explicit controls.
- Unexpected source mutation outside approved quarantine actions.

## Rollback / Recovery Notes

- Restore DB from latest backup before rerun if state becomes inconsistent.
- Quarantined files are reversible from quarantine location; no permanent delete in v0.
- Stop workflow immediately on safety gate failure and re-evaluate before retry.

## Known Limitations

- Encryption/decryption deferred.
- OneDrive/cloud publish deferred.
- Cleanup is quarantine-only and still operator-supervised.
- Duplicate model has mixed file-level vs instance-level semantics handled by workflow logic.

## What Must Not Happen

- No OneDrive/rclone calls in SUC_001 lifecycle.
- No permanent delete.
- No ungated real DB writes.
- No whole-folder cleanup operations.
- No source cleanup before UC_008 verification success.
