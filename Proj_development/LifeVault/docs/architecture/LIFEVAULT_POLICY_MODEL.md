# LIFEVAULT_POLICY_MODEL.md

## Purpose

Define reusable policy objects for lifecycle, retention, sensitivity, storage, and safety gates across all LifeVault capabilities.

## Retention Policy as Object

Retention must be modeled as reusable policy objects, not only free-text fields.

Default policy:

- `default_lifetime_user_use`

Meaning:

- keep indefinitely while LifeVault is actively used by Sean
- no auto-delete
- no auto-expire
- no auto-archive
- maintenance/report visibility only unless explicit replacement policy is attached

Future policy examples:

- `tax_7_year_review`
- `job_package_2_year_review`
- `temporary_90_day_review`
- `legal_hold`
- `family_archive`
- `cold_storage_candidate`
- `delete_candidate_manual_only`

## Sensitivity Policy

Current simplified levels:

- `normal`
- `sensitive`

Sensitive policy expectations:

- encrypted at rest/in transit in later security phase
- decrypted only for approved use sessions
- default unlock session 4 hours (configurable)
- searchable metadata remains visible
- sensitive payload values remain encrypted

Sensitive note pattern:

- `public_hint` searchable
- `encrypted_body` protected

## Cleanup Policy

v0 cleanup policy:

- quarantine/archive only
- no permanent delete
- explicit approval required
- verification prerequisite required

## Storage Policy

Supports multi-destination tracking and eventual storage governance across local/cloud/encrypted/archive targets.

v0 still operates in local-first mode with cloud/encryption deferred.

## Gate/Approval Policy

Core gates:

- human approval for risky transitions
- dry-run first for publish/verify/cleanup classes
- real DB confirmation flags for real operational DB actions
- no OneDrive/rclone actions unless corresponding workflow phase is explicitly approved

## Policy Attachment Scope

Policies may attach to:

- individual `vault_item`
- item groups (note folders, project groups, maintenance groups)
- capability workflows (publish, verify, cleanup)
- task/project/group objects for queue governance

Task/project model reference:

- `docs/architecture/LIFEVAULT_TASK_PROJECT_MODEL.md`

## Policy Evolution Strategy

- start simple policy defaults
- keep policy objects explicit and versionable
- evolve per capability cycle without blocking thin-slice delivery
