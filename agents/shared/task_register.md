# Task Register

Track active and completed tasks to avoid losing continuity.

## Status Values

- `planned`
- `in_progress`
- `done`
- `blocked`

## Tasks

| Task ID | Summary | Status | Updated On | Notes |
|---|---|---|---|---|
| TB-20260401-01 | Bootstrap control protocol and continuity files | done | 2026-04-01 | Initial setup |
| TB-20260401-02 | Rebalance controls for bounded autonomy and durable memory | done | 2026-04-01 | Added context index and open loops |
| TB-20260401-03 | Add approval matrix and command allowlist controls | done | 2026-04-01 | Closed LOOP-001 |
| TB-20260401-04 | Implement portable machine profiles and encrypted secret bootstrap | done | 2026-04-01 | Added env core scripts and docs |
| TB-20260401-05 | Add guided one-command portable bootstrap script | done | 2026-04-01 | Added `scripts/env/bootstrap_all.ps1` and docs updates |
| TB-20260401-06 | Add architecture-grade ADR governance and tooling | done | 2026-04-01 | Added ADR index, ADR records, and generator script |
| TB-20260401-07 | Import credential inventory from legacy `D:\workspace` into local StudyBook secrets bundle | done | 2026-04-01 | Created source manifest and staging import |
| TB-20260401-08 | Encrypt imported credentials and remove plaintext secret files | done | 2026-04-01 | Created encrypted secret files and deleted plaintext |
| TB-20260401-09 | Add operations runbook folder for self-service usage | done | 2026-04-01 | Added operations guides |
| TB-20260402-01 | Add Claude subscription renewal tracker in operations docs | done | 2026-04-02 | Added subscription runbook |
| TB-20260402-02 | Create ZeroToHero infra-first migration execution system and tracking board | done | 2026-04-02 | Added execution system and migration board |
| TB-20260402-03 | Execute BATCH-INFRA-01 (compose contract and env/startup scripts) | done | 2026-04-02 | Implemented as part of `_infra` baseline completion |
| TB-20260402-04 | Extract TalksWithClaude value and create workspace-to-target shift/lift placement plan | done | 2026-04-02 | Added extraction doc + placement map |
| TB-20260402-05 | Execute infra shift-lift from workspace setup assets into target `_infra` | done | 2026-04-02 | Completed in StudyBook after canonical target correction |
| TB-20260402-06 | Finalize reproducible infra script pack, cloud registry baseline, and StudyBook-only planning retarget | done | 2026-04-02 | Added `_infra/scripts`, cloud registry doc, board/path retarget, health validation |
| TB-20260402-07 | Shift/lift validated Technologies notebooks into canonical StudyBook track paths | planned | 2026-04-02 | Next batch: `M-011` / `BATCH-MIG-02A` |
| TB-20260402-08 | Add Docker service dictionary doc and cross-links for agent discoverability | done | 2026-04-02 | Added operations dictionary and linked from infra/operations readmes |
| TB-20260402-09 | Capture MongoDB Atlas credentials into local secure env flow and add provider mapping docs | done | 2026-04-02 | Stored in ignored _infra/env/.env.local; registry updated without plaintext secrets |
| TB-20260402-10 | Verify GCP key readiness and register missing-real-key status in StudyBook tracking docs | done | 2026-04-02 | Confirmed all workspace GCP key files are placeholders; documented exact next action |
| TB-20260402-11 | Ingest real GCP SA key securely and wire StudyBook local env to protected key path | done | 2026-04-02 | Key stored under user-protected folder; .env.local updated with path/project metadata |
| TB-20260402-12 | Create connection proofs POC folder with MongoDB and GCP sample scripts | done | 2026-04-02 | Added read-only proof scripts under poc/connection_proofs/python and updated proof README |
| TB-20260402-13 | Improve MongoDB connection proof diagnostics for Atlas TLS handshake troubleshooting | done | 2026-04-02 | Added SSL/OpenSSL/PyMongo diagnostics and TLS options to mongo proof script |
| TB-20260402-14 | Resolve GitHub push protection block by removing leaked token from local commit history and repushing | done | 2026-04-02 | Rebuilt two local commits without 	emp/TalksWithClaude.md, kept backup branch, push succeeded |
| TB-20260402-15 | Improve GCP connection proof semantics for partial API availability and strict mode fallback | done | 2026-04-02 | Default success now accepts any successful read-only probe; added --require-project-lookup strict mode and clearer diagnostics |
| TB-20260402-16 | Add AWS credential portability workflow and AWS STS connection proof | done | 2026-04-02 | AWS STS check succeeded with local `study`; encrypted bundle created; proof now auto-resolves profiles to avoid hardcoded defaults |
| TB-20260402-17 | Add machine-local DPAPI seed flow for passphrase-free secret decrypt across agent runs | done | 2026-04-02 | Added local seed register/remove scripts, env_core auto-seed passphrase resolution, and validated noninteractive env load |
| TB-20260402-18 | Polish Azure proof wiring across README/env template/registry status | done | 2026-04-02 | Added Azure proof docs, AZURE_* env placeholders, fixed gitignore so `_infra/env/.env.example` is tracked, and updated cloud registry to proof_verified_local |
| TB-20260402-19 | Add Databricks connection proof and wire registry/env/readme metadata | done | 2026-04-02 | Databricks host/email captured, proof script added; blocked for live success until PAT is generated and stored as DATABRICKS_TOKEN |
| TB-20260402-20 | Enforce encrypted-secrets system-of-record flow and add direct seed-backed secret update command | done | 2026-04-02 | Added `set_secret.ps1`, updated secrets workflow/memory, and captured Databricks workspace ID in registry |
| TB-20260402-21 | Fix Databricks proof credential resolution by adding encrypted-secret fallback and validate host autoload | done | 2026-04-02 | Proof now reads host/token from seed-backed encrypted secrets; host injected into asuspc encrypted file; remaining blocker is PAT token value |
| TB-20260402-22 | Add secure prompt mode for seed-backed secret updates and validate Databricks token-missing root cause | done | 2026-04-02 | `set_secret.ps1` now supports `-PromptSecretKey`; validated `DATABRICKS_HOST` present and `DATABRICKS_TOKEN` missing in encrypted secrets |
| TB-20260402-23 | Persist Databricks PAT in encrypted secret records and normalize shared-machine resolution | done | 2026-04-02 | PAT saved to encrypted `asuspc` and `shared` secret files; remaining validation depends on local shell/network reachability |
| TB-20260402-24 | Close Databricks connectivity loop after successful proof and sync registry/board statuses | done | 2026-04-02 | Databricks proof returned `ok: true`; C-005 marked done and LOOP-016 closed |
| TB-20260402-25 | Ingest Snowflake creds into encrypted flow, add Snowflake proof, and scrub plaintext from workspace markdown | done | 2026-04-02 | Encrypted SNOWFLAKE_* captured, proof script added, plaintext scrubbed in target files; connectivity currently blocked on Snowflake backend connect error 250001 |
| TB-20260402-26 | Close Snowflake validation blocker after successful owner-shell proof and sync tracking | done | 2026-04-02 | Snowflake proof now `ok: true`; C-003 marked done and LOOP-017 closed |
| TB-20260402-27 | Add grouped Docker connection POC scripts for all local infra services with simple operations | done | 2026-04-02 | Added core/streaming/pipeline/observability Docker proof scripts + master runner and README mapping |
| TB-20260402-28 | Add individual Python Docker proof scripts per service under poc/connection_proofs/python | done | 2026-04-02 | Added 15 per-service Python Docker proof wrappers plus shared common module and README usage section |
| TB-20260402-29 | Add portable JupyterLab Docker service with StudyBook bind-mount and proof wiring | done | 2026-04-02 | Added jupyterlab to pipeline/full compose with ../../ bind mount, env/doc updates, and Docker proof scripts |

| TB-20260402-32 | Execute M-002 coding assets migration with immediate Workspace decommission | done | 2026-04-02 | Ran scripts/migration/run_m002_coding_assets.ps1 -Execute -DeleteSource; run_20260402_113935 created manifests, backup, and removed scoped D:\Workspace sources |
| TB-20260402-33 | Create first coding challenges study manual and roadmap draft from migrated manifests | done | 2026-04-02 | Added coding_challenges/STUDY_MANUAL_V1.md and coding_challenges/ROADMAP_DRAFT_V1.md based on INDEX/ROADMAP_INPUT_MANIFEST/TOPIC_COVERAGE |
