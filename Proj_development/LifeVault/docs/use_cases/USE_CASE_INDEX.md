# USE_CASE_INDEX.md

| ID | Name | Status | Risk | Dependencies | Next Action |
|---|---|---|---|---|---|
| LV_INGEST_FOLDER_V0 | Operator Workflow (UC_001 + UC_003) | implemented (temp-only) | medium | UC_001, UC_003, explicit pod approval gate | Run temp smoke and then guarded real run with explicit operator approval |
| UC_001 | Ingest Folder Proposal | implemented / real-folder validated | medium | paths config, proposal schema, `docs/contracts/UC_001_PROPOSAL_JSON_CONTRACT.md` | Use validated output as intake gate before UC_003 planning |
| UC_002 | Detect Sensitive Files by Metadata and Filename Rules | partially implemented through UC_001 v0 | high | UC_001 metadata outputs, safety rules | Decide if standalone UC_002 command is needed beyond UC_001 embedded hints |
| UC_003 | Create Onboarding Pod | implemented (temp-only) | high | UC_001 approved proposal, UC_002 sensitivity pass, folder setup script, `docs/use_cases/UC_003_CREATE_ONBOARDING_POD_WORKFLOW_SPEC.md`, `docs/contracts/UC_003_POD_PROFILE_AND_MANIFEST_CONTRACT.md` | Validate temp-only behavior and prepare guarded real-mode rollout checklist |
| UC_004 | Index Pod to Database | implemented (temp-only) | high | migration runner, schema v0, UC_003, `docs/use_cases/UC_004_INDEX_POD_TO_DATABASE_WORKFLOW_SPEC.md` | Validate temp indexing + dry-run and keep real DB guard in place |
| UC_011 | Detect Sensitive Content (Gated Future) | planned / future gated content scan | high | UC_004 indexed references, explicit approval, storage policy | Define gated extraction workflow and redaction pipeline |
| UC_005 | Search Memory Without Hydration | implemented | medium | UC_004 indexed metadata, `docs/use_cases/UC_005_SEARCH_MEMORY_WITHOUT_HYDRATION_WORKFLOW_SPEC.md` | Use read-only metadata queries for pod/file/review discovery |
| UC_006 | Publish Approved Files to Vault | planned | high | UC_004 review/publish states, UC_007 verification design | Design explicit publish workflow with checkpoints |
| UC_007 | Verify Vault Copy | planned | high | UC_006 publish output | Define hash/path verification and audit logging |
| UC_008 | Cleanup Source After Verification | planned | high | UC_007 verified copy, explicit approval | Define guarded cleanup policy and reversible steps |
| UC_009 | Ingest Code Folder | planned | medium | UC_001 proposal flow, UC_002 metadata sensitivity | Define code-aware metadata extraction without secret leakage |
| UC_010 | Backup/Restore Database | designed | high | backup policy, operations runbook | Implement backup/restore scripts after migration runner hardening |
