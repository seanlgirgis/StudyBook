# Open Loops

Track incomplete but in-scope work items so sessions resume cleanly.

## Status Meanings

- `open`
- `in_progress`
- `blocked`
- `closed`

## Items

| Loop ID | Related Task ID | Item | Status | Next Action | Updated On |
|---|---|---|---|---|---|
| LOOP-001 | TB-20260401-01 | Add approval matrix and command allowlist policy files | closed | none | 2026-04-01 |
| LOOP-002 | TB-20260401-04 | Create encrypted secrets files for shared and per-machine profiles | closed | none | 2026-04-01 |
| LOOP-003 | TB-20260401-07 | Promote imported legacy credentials into encrypted StudyBook secret files | closed | none | 2026-04-01 |
| LOOP-004 | TB-20260402-07 | Execute notebook migration backlog for validated Technologies set (`M-011`) | closed | none | 2026-04-02 |
| LOOP-005 | TB-20260402-06 | Complete cloud secret routing + migration secret sanitization gate (`C-002`, `M-014`) | in_progress | Secret-scan gate passed for M-011/M-013/M-008/ML_AI run (`secret_hits=0`); continue provider secret mapping + remaining migration waves | 2026-04-02 |
| LOOP-006 | TB-20260402-08 | Create Docker service dictionary with concise purpose notes per service | closed | none | 2026-04-02 |
| LOOP-007 | TB-20260402-09 | Migrate MongoDB credential from local .env.local into encrypted secret files and rotate Atlas password/token | open | Run bootstrap encryption with passphrase and then rotate MongoDB password | 2026-04-02 |
| LOOP-008 | TB-20260402-11 | Normalize legacy workspace GCP key placeholders after secure key ingestion | in_progress | Decide if legacy hardcoded path is still required; if not, delete placeholder duplicates in `D:\Workspace\Technologies\_setup` | 2026-04-02 |
| LOOP-009 | TB-20260402-12 | Add connection proofs POC scripts for MongoDB and GCP | closed | none | 2026-04-02 |
| LOOP-010 | TB-20260402-13 | Improve Mongo proof diagnostics to troubleshoot Atlas TLS failures | closed | none | 2026-04-02 |
| LOOP-011 | TB-20260402-14 | Clear push-protection secret violation from outgoing commit range | closed | none | 2026-04-02 |
| LOOP-012 | TB-20260402-15 | Align GCP proof pass/fail logic with partial API availability and add strict toggle | closed | none | 2026-04-02 |
| LOOP-013 | TB-20260402-16 | Encrypt AWS profile bundle into StudyBook secrets for cross-machine restore | closed | Bundle created and plaintext removed | 2026-04-02 |
| LOOP-014 | TB-20260402-17 | Enable machine-local seed-backed secret passphrase resolution for noninteractive agent runs | closed | Seed file registered and env bootstrap validated with passphrase env var unset | 2026-04-02 |
| LOOP-015 | TB-20260402-18 | Finish Azure proof documentation and registry status alignment | closed | README/env template/registry updated and validated | 2026-04-02 |
| LOOP-016 | TB-20260402-19 | Complete Databricks proof by generating PAT and storing DATABRICKS_TOKEN in local secret/env flow | closed | none | 2026-04-02 |
| LOOP-017 | TB-20260402-25 | Complete Snowflake proof after backend-connect blocker (`250001`) by validating network/account policy and rerunning read-only proof | closed | none | 2026-04-02 |
| LOOP-018 | TB-20260402-27 | Run Docker exec portions of new group POCs from owner shell (sandbox here has docker API permission limits) and capture any service-specific fixes | closed | none | 2026-04-02 |
| LOOP-019 | TB-20260402-29 | Add portable JupyterLab Docker service and proof coverage | closed | none | 2026-04-02 |

| LOOP-020 | TB-20260402-32 | Execute coding assets shift/lift and decommission migrated D:\Workspace sources | closed | none | 2026-04-02 |
| LOOP-021 | TB-20260402-33 | Produce first manuals/roadmaps-ready docs from coding_challenges manifests | closed | none | 2026-04-02 |
| LOOP-022 | TB-20260402-34 | Complete Databases shift/lift from Workspace into tracks/08_databases and _prompts/legacy/databases | closed | none | 2026-04-02 |
| LOOP-023 | TB-20260402-36 | Reconcile duplicate-suffixed Technologies legacy prompts produced during conflict-safe migration | open | Review `D:\StudyBook\temp\migration_meta\run_20260402_121903\conflicts_report.md` and decide keep-vs-dedupe policy for `__dupNNN` files | 2026-04-02 |
| LOOP-024 | TB-20260402-37 | Decommission migrated Technologies + DE_Interview sources using move-map safe deletion | closed | none | 2026-04-02 |
| LOOP-025 | TB-20260402-38 | Reconcile migration board statuses with completed source-deletion reality for M-003/M-012 and add residual-Technologies decommission plan | open | Decide whether to decommission remaining `D:\Workspace\Technologies` non-migrated assets or retain as legacy runtime island, then update board accordingly | 2026-04-02 |
