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
| LOOP-004 | TB-20260402-07 | Execute notebook migration backlog for validated Technologies set (`M-011`) | open | Run `BATCH-MIG-02A` and smoke-test one notebook per migrated track | 2026-04-02 |
| LOOP-005 | TB-20260402-06 | Complete cloud secret routing + migration secret sanitization gate (`C-002`, `M-014`) | in_progress | Populate encrypted key mapping and run secret scan during notebook/prompt migration | 2026-04-02 |
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


