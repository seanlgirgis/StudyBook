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
