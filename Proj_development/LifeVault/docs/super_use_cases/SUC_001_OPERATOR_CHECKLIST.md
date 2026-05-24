# SUC_001_OPERATOR_CHECKLIST.md

## SUC_001 Operator Checklist (v0)

- [ ] Confirm one-writer mode and current branch/checkpoint.
- [ ] Run `..\..\env_setter.ps1`.
- [ ] Run DB backup before write stages.
- [ ] Confirm source path and story.

### UC_001 Proposal

- [ ] Run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc001_proposal.ps1 -SourcePath "<source_path>" -Story "<story_optional>"`
- [ ] Verify proposal artifacts exist.
- [ ] Stop if proposal status is failed.

### UC_003 Pod

- [ ] Run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc003_create_pod.ps1 -ProposalPath "<proposal_json>" -Approved`
- [ ] Verify pod structure exists.
- [ ] Stop if copy errors are present.

### UC_004 Index

- [ ] Dry-run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod_path>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -DryRun -RealDbConfirm`
- [ ] Approved:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc004_index_pod.ps1 -PodPath "<pod_path>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -Approved -RealDbConfirm`
- [ ] Stop if index fails or duplicates/ref integrity issues appear.

### UC_005 Search

- [ ] Run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc005_search.ps1 -PodId "<pod_id>"`
- [ ] Verify pod/file rows are discoverable.

### UC_006 + UC_006B Review

- [ ] Review items:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -ListItems -RealDbConfirm`
- [ ] Check readiness:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc006_review.ps1 -PodId "<pod_id>" -PublishReadiness -RealDbConfirm`
- [ ] Decision point: proceed only with intended `ready_to_publish` items.

### UC_007 Publish

- [ ] Dry-run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -DryRun -RealDbConfirm`
- [ ] Approved:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc007_publish_local.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -ApprovedPublish -RealDbConfirm`
- [ ] Stop if publish manifest has failures/conflicts.

### UC_008 Verify

- [ ] Dry-run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -DryRun -RealDbConfirm`
- [ ] Approved:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc008_verify_publish.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -VaultRoot "D:\AI_Lab\LifeVault\vault_local" -ApprovedVerify -RealDbConfirm`
- [ ] Stop if verify manifest has mismatches.

### UC_009 Quarantine Cleanup

- [ ] Dry-run:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -QuarantineRoot "D:\AI_Lab\LifeVault\cleanup_quarantine" -DryRun -RealDbConfirm`
- [ ] Approved:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\run_uc009_cleanup_quarantine.ps1 -PodId "<pod_id>" -DbPath "D:\AI_Lab\LifeVault\db\lifevault.sqlite" -QuarantineRoot "D:\AI_Lab\LifeVault\cleanup_quarantine" -ApprovedCleanup -RealDbConfirm`
- [ ] Confirm only intended candidates moved to quarantine.

## Stop Conditions

- Any stage fails safety gates.
- Unexpected file movement/copy behavior.
- Unexpected DB write outside approved stages.
- Any mismatch in UC_008 verification.

## Safety Reminders

- No OneDrive/rclone calls in SUC_001 flow.
- No permanent delete in v0.
- No cleanup before UC_008 verification success.
- Sensitive/highly_sensitive actions require explicit approvals/gates.
