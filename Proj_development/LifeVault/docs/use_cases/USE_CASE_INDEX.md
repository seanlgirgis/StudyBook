# USE_CASE_INDEX.md

| ID | Name | Status | Risk | Dependencies | Next Action |
|---|---|---|---|---|---|
| UC_001 | Ingest Folder Proposal | designed | medium | paths config, proposal schema | Implement proposal-only scanner (no copy/no DB write) |
| UC_002 | Detect Sensitive Files | planned | high | UC_001 metadata outputs, safety rules | Define sensitivity heuristics and false-positive review flow |
| UC_003 | Create Onboarding Pod | planned | high | UC_001, UC_002, folder setup script | Design copy-only pod creation with approval gate |
| UC_004 | Index Pod to Database | planned | high | migration runner, schema v0 | Implement temp-DB first indexing pipeline |
| UC_005 | Search Memory Without Hydration | planned | medium | UC_004 indexed metadata | Define query UX over DB metadata only |
| UC_006 | Publish Approved Files to Vault | planned | high | UC_004 review/publish states | Design explicit publish workflow with checkpoints |
| UC_007 | Verify Vault Copy | planned | high | UC_006 publish output | Define hash/path verification and audit logging |
| UC_008 | Cleanup Source After Verification | planned | high | UC_007 verified copy, explicit approval | Define guarded cleanup policy and reversible steps |
| UC_009 | Ingest Code Folder | planned | medium | UC_001 proposal flow, UC_002 sensitivity | Define code-aware metadata extraction without secret leakage |
| UC_010 | Backup/Restore Database | designed | high | backup policy, operations runbook | Implement backup/restore scripts after migration runner hardening |