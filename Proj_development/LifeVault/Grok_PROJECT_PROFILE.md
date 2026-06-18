# Grok Project Profile — LifeVault

**Path:** `D:\Workarea\StudyBook\Proj_development\LifeVault`  
**Operational path:** `D:\AI_Lab\LifeVault`  
**Type:** hybrid (application workflows + knowledge vault)  
**Profile version:** 2026-06-17

## One-Line Summary

Personal AI-assisted file and knowledge vault — SQLite metadata map, onboarding pods, copy-first publish pipeline; one proven v0 folder lifecycle (`SUC_006`).

## Does this project

- Govern local folder/file lifecycle (`UC_001`–`UC_009`)
- Maintain operational DB and clean vault under `D:\AI_Lab\LifeVault`
- Build notes, Streamlit help console, and future vault-item capabilities
- Enforce human-approve, no-delete-by-default, quarantine-only v0 cleanup

## Does not

- Replace `local_memory` runbooks or `ALOK` work-learning
- Host Coursera/DataCamp packages (`learning`)
- Run rclone/cloud publish or permanent delete without approved workflow
- Store secrets or live operational DB in Git

## Route signals — keywords

`LifeVault`, `lifevault`, `SUC_`, `UC_00`, `vault_item`, `onboarding pod`, `AI_Lab`, `lifevault.sqlite`, `quarantine`, `publish local`, `Streamlit help console`

## Route signals — paths

`D:\Workarea\StudyBook\Proj_development\LifeVault`, `D:\AI_Lab\LifeVault`, `src/lifevault/`, `docs/super_use_cases/`

## Default work mode

`feature` (scoped workflow or module); use `bite_sized` for doc-only reconciliation

## Read first (child agents)

1. `GROK_AGENTS.md`
2. `GROK_RUNBOOK.md`
3. `agents/codex/LIFEVAULT_BOOTSTRAP.md`
4. Task-specific docs/paths only

## Hard rules

- AI suggests; human approves
- Two-root model: dev repo vs `D:\AI_Lab\LifeVault`
- Codex implements; Grok guards `GROK_*` and scopes work
- Launch: `C:\scripts\start_grok_lifevault.ps1`