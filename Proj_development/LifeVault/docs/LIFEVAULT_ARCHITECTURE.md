# LIFEVAULT_ARCHITECTURE.md

## Layers

1. Intake: local folders, OneDrive remote views, old drives, exports, archives.
2. Onboarding pods: controlled working copies for review and enrichment.
3. Metadata pipeline: provenance, sensitivity, lifecycle temperature, duplicate status, and searchable context.
4. Datastore: `D:\AI_Lab\LifeVault\db\lifevault.sqlite` as the primary map for discovery and governance decisions.
5. Publish pipeline: explicit human-approved promotion to clean vault.
6. Search and memory: queryable map without requiring full OneDrive hydration.

## Writer/Reader Model (v0)

- One writer machine, many reader/search machines.
- First writer machine: ASUS PC.
- Live DB is not synced for concurrent writes.
- Portable artifacts for cross-machine use are backups and exports, not active multi-writer DB replicas.

## Delivery Method

- Architecture delivery is anchored to use cases in `docs/use_cases/USE_CASE_INDEX.md`.
- Business, technical, safety, and data constraints are tracked in `docs/requirements/`.
- Sensitivity handling is staged: metadata/filename rules first, content-based detection only in explicit approved workflows.
- Content extraction must follow storage, privacy, and backup policy controls.
