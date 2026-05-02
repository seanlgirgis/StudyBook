# CHANGELOG.md

## 2026-05-01
### Added
- Permanent project memory files: `DAILY_LOG.md`, `DECISIONS.md`, `KNOWN_ISSUES.md`, `CHANGELOG.md`.
- Milestone 1 static shell files and content in `pocs/01_static_site_shell`:
  - `website/index.html`
  - `website/assets/styles.css`
  - `website/assets/chat-widget.js`
  - `notes/what_this_teaches.md`
  - `notes/questions.md`
- `aux_scripts/` helper utilities:
  - `aux_scripts/README.md`
  - `aux_scripts/show_tree.ps1`
  - `aux_scripts/zip_folder_for_chatgpt.ps1`
  - `aux_scripts/check_poc_static_site.ps1`
  - `aux_scripts/snapshot_project_state.ps1`
- Milestone 1 Cloudflare static smoke-test record:
  - `pocs/01_static_site_shell/notes/cloudflare_static_smoke_test.md`

### Changed
- `AGENTS.md` now enforces:
  - environment bootstrap command before Python/pytest/pip/FastAPI/scripts
  - closed-loop reporting format after every task
  - expanded required read/update file sets
  - milestone stop-rule escalation behavior
- `PROJECT_STATE.md` now states the closed-loop project-control protocol exists.
- `TASK_BOARD.md` now marks permanent agent memory / closed-loop protocol as done.
- `HANDOFF.md` now explicitly keeps the next task at `pocs/01_static_site_shell` only.
- `pocs/01_static_site_shell/README.md` now documents purpose, files, run steps, learning outcomes, exclusions, and next step.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, and `HANDOFF.md` now reflect Milestone 1 static site shell completion and next review step.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect aux script utility support and validation workflow.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now include Milestone 1 Cloudflare static-hosting smoke-test documentation status.

## 2026-05-02
### Added
- Milestone 2 synthetic business documents and notes in `pocs/02_fake_business_docs`:
  - `data/home_services_demo/company_profile.md`
  - `data/home_services_demo/service_area.md`
  - `data/home_services_demo/business_hours.md`
  - `data/home_services_demo/hvac_repair_policy.md`
  - `data/home_services_demo/ac_replacement_estimates.md`
  - `data/home_services_demo/plumbing_services.md`
  - `data/home_services_demo/water_heater_policy.md`
  - `data/home_services_demo/appliance_repair_policy.md`
  - `data/home_services_demo/maintenance_plan.md`
  - `data/home_services_demo/coupon_policy.md`
  - `data/home_services_demo/scheduling_policy.md`
  - `data/home_services_demo/financing_policy.md`
  - `data/home_services_demo/warranty_policy.md`
  - `data/home_services_demo/escalation_rules.md`
  - `data/home_services_demo/intake_script.md`
  - `data/home_services_demo/faq.md`
  - `notes/retrieval_questions.md`
  - `notes/what_good_answers_should_include.md`
  - `notes/document_design_notes.md`

### Changed
- `pocs/02_fake_business_docs/README.md` now defines purpose, file map, synthetic warning, and next milestone.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect Milestone 2 completion and next-step retrieval POC direction.
