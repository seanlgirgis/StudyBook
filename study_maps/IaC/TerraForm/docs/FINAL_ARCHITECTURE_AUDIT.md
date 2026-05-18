# Final Architecture Audit

## Scope
Final architecture cleanup to enforce strict separation:
- `study_maps/IaC/TerraForm` = learning product, deployable study package, course front door, maps, study pages, Q&A, flashcards, conceptual/interview materials.
- `tutorials/IaC/TerraForm` = hands-on lab bench only.

## What Was Misplaced
- Course-home mapResource links in topic JSON pointed to tutorials course hub:
  - `../../../../tutorials/IaC/TerraForm/index.html`
- Non-lab study content lived under tutorials:
  - `10_interview_qa_consolidation`
  - `11_interview_flashcards`
  - `study_pages`
  - `00_iac_why_terraform_exists`
  - `01_terraform_1000_foot_view`
- Non-runnable conceptual/interview files inside `09_aws_observability_interview_bridge` were mixed with lab-area content.

## What Moved
Copied into `study_maps` first, then tutorials copies removed after validation:

### Moved to `study_maps/IaC/TerraForm/course`
- `course/10_interview_qa_consolidation`
- `course/11_interview_flashcards`
- `course/09_aws_observability_interview_bridge/interview`
- `course/09_aws_observability_interview_bridge/checklists`
- `course/09_aws_observability_interview_bridge/conceptual_examples`
- `course/09_aws_observability_interview_bridge/no_cli_required.txt`
- `course/09_aws_observability_interview_bridge/interview_bridge_concepts.txt`

### Moved to `study_maps/IaC/TerraForm/study_pages`
- `study_pages/03_core_workflow`
- `study_pages/00_iac_why_terraform_exists`
- `study_pages/01_terraform_1000_foot_view`

## What Stayed In Tutorials And Why
Stayed because they are hands-on lab material:
- `02_core_workflow`
- `03_state_drift_backends`
- `04_providers_resources`
- `05_variables_outputs_locals`
- `06_modules_reuse`
- `07_environments_workspaces`
- `08_safety_team_workflow_cicd`
- `labs/`

Notes:
- Tutorials hub and README were rewritten as lab-bench only.
- Non-lab folders were removed from tutorials after replacement verification.

## Old Links Removed
- Source topics repaired:
  - Replaced only course-home links:
    - old: `../../../../tutorials/IaC/TerraForm/index.html`
    - new: `../index.html`
- True lab links to `../../../../tutorials/IaC/TerraForm/<lab>/...` were preserved.
- Full map outputs rebuilt so generated HTML no longer contains old course-home links.

## Files Updated (High Level)
- `study_maps/IaC/TerraForm/topics/*.studybubble.json` (course-home href repair only)
- `study_maps/IaC/TerraForm/index.html` (study front door links now point to study_maps course/study pages)
- `tutorials/IaC/TerraForm/index.html` (lab-only hub)
- `tutorials/IaC/TerraForm/README.md` (lab-only scope)
- `study_maps/IaC/TerraForm/STUDYBUBBLE_SESSION_STATE.md`

## Commands Run
```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
cd D:\Workarea\StudyBook\study_maps\IaC\TerraForm
bubbles build <each-topic-id>
```
Also used filesystem copy/remove and `rg` validation scans.

## Build Result
- Rebuilt all 10 maps successfully.
- Generated outputs refreshed under:
  - `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\*.html`

## Validation Summary
- Old course-home link removed from topics: PASS.
- Old course-home link removed from generated outputs: PASS.
- True lab links to tutorials preserved: PASS.
- Q&A/flashcards now present under `study_maps/course`: PASS.
- `study_pages` no longer under tutorials: PASS.
- `00` and `01` no longer under tutorials: PASS.
- Tutorials hub/README describe tutorials as lab-only: PASS.
- `study_maps/.../index.html` is the primary front door: PASS.

## Remaining Manual-Review Items
- Confirm preferred long-term location and naming for conceptual 09 hub page in `study_maps/course` (if a dedicated index page is desired there).
- Spot-check browser navigation from mapResources and hub pages.

## Final Opening Path
`D:\Workarea\StudyBook\study_maps\IaC\TerraForm\index.html`
