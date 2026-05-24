# LIFEVAULT_PROJECT_TASK_SEED.md

## Purpose

High-level project/task-group/task seed for LifeVault cyclic planning.
This is a planning seed, not a complete backlog.

## Project

- **LifeVault Buildout**

## Seed Task Groups

### 1. Foundation / Vault Item Model

- **Task:** Document vault_item model baseline
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: `LIFEVAULT_VAULT_ITEM_MODEL.md` created
- **Task:** Document policy model baseline
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: `LIFEVAULT_POLICY_MODEL.md` created
- **Task:** Add search/report view for foundational models
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: add read-only architecture status page

### 2. SUC_001 / Universal Capture and Ingest

- **Task:** Design v0 broad capture adapter plan
  - status: open
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: include files/folders/URLs/notes intake lanes
- **Task:** Implement thin slice beyond folders
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: next likely URL or notes intake
- **Task:** Create acceptance checklist
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: after second slice exists

### 3. SUC_006 / File and Folder Lifecycle

- **Task:** Validate SUC_006 repeat run
  - status: open
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: run second tiny safe folder acceptance
- **Task:** Add search/report lifecycle view
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: summarize publish/verify/quarantine states
- **Task:** Proven v0 lifecycle baseline
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: first vertical slice proven with apod

### 4. SUC_005 / Notes and Knowledge Memory

- **Task:** Design notes v0
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: SUC_005 note model + template/filename contracts documented
- **Task:** Implement thin slice
  - status: done
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: one safe note create/search path implemented (markdown + frontmatter parsing, no DB writes)
- **Task:** Add search/report view
  - status: done
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: notes search/list thin slice implemented (standalone + note_folder notes)
- **Task:** Create acceptance checklist
  - status: done
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: `SUC_005_ACCEPTANCE_CHECKLIST.md` created

### 5. SUC_010 / Secrets and Sensitive Records

- **Task:** Design v0 boundary and policy
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: define LifeVault vs password-manager split
- **Task:** Create acceptance checklist
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: include non-destructive validation only

### 6. SUC_014 / Encryption, Decryption, and Secure View

- **Task:** Design sensitive unlock model
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: target 4-hour unlock session default
- **Task:** Design thin slice implementation boundary
  - status: open
  - priority: P2
  - intake_date: TBD
  - due_date: none
  - notes: no implementation until approved cycle

### 7. SUC_015 / Streamlit Control Center / Agent Console

- **Task:** Design read-only dashboard v0
  - status: open
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: capability map/status/recent activity
- **Task:** Implement thin slice read-only view
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: no write actions in first cut

### 8. SUC_018 / Physical Storage Inventory

- **Task:** Design v0 physical model
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: container recursion + item metadata
- **Task:** Create acceptance checklist
  - status: open
  - priority: P2
  - intake_date: TBD
  - due_date: none
  - notes: include location verification rules

### 9. SUC_019 / Contacts and People Vault

- **Task:** Design contacts import v0
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: ingest fast, cleanup later
- **Task:** Add maintenance queue
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: `contact_merge_queue`

### 10. SUC_020 / Email and Attachment Vault

- **Task:** Design mbox import source v0
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: parse/harvest/summarize boundaries
- **Task:** Add maintenance queue
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: `email_prune_queue`, `attachment_dedup_queue`

### 11. SUC_021 / Tasks, Projects, and Maintenance Queues

- **Task:** Design task/project model
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: `LIFEVAULT_TASK_PROJECT_MODEL.md` created
- **Task:** Create seed board
  - status: done
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: this file created
- **Task:** Add search/report view
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: read-only task group progress board

### 12. Reporting / Audit / Maintenance

- **Task:** Design v0 governance report pack
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: inventory/duplicate/sensitivity/audit reports
- **Task:** Add maintenance queue
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: reporting consistency and stale-state checks

### 13. Backup / Restore / Portability

- **Task:** Create acceptance checklist
  - status: open
  - priority: P0
  - intake_date: TBD
  - due_date: none
  - notes: backup/restore drill with checksum validation
- **Task:** Add search/report view
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: backup freshness and restore readiness dashboard

### 14. Cloud / OneDrive / Multi-Destination Storage

- **Task:** Design v0 cloud storage tracking
  - status: open
  - priority: P1
  - intake_date: TBD
  - due_date: none
  - notes: tracking before sync execution
- **Task:** Implement thin slice
  - status: deferred
  - priority: P2
  - intake_date: TBD
  - due_date: none
  - notes: blocked pending encryption design

## Completed Areas (Current Baseline)

- SUC_001 / File-Folder lifecycle v0 proven
- SUC_021 task/project model design completed
- 1000-foot capability map completed
- vault_item model design completed
- policy model design completed

## How to Use This Seed

- Expand one task group at a time.
- Keep cyclical development; avoid perfecting one lane for months.
- Compare current state to target capability before each implementation bite.
- Generate maintenance tasks later from system findings.
- Tasks recommend work; scripts execute only through explicit approval gates.
