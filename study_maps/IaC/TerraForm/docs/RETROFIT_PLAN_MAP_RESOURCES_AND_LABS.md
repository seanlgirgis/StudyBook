# LearnTerraform Retrofit Plan — Map Resources, Tutorials, and Labs

## Scope and constraints for this run
- Audit and planning only.
- No map rewrites, no new maps, no lab creation, no StudyBubble engine changes.
- Retrofit objective: stabilize existing maps before adding new ones.

## 1) Current inventory

### Container and governance
- Container root: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm`
- `bubbles.ini`: present, single-file mode, default topic `terraform_1000_foot_view`
- Governance/docs present: `README.md`, `STUDYBUBBLE_SESSION_STATE.md`, `docs\CODEX_CONSTITUTION.md`, `docs\LEARN_TERRAFORM_CURRICULUM_STATE.md`

### Existing topic JSON files
- `topics\iac_why_terraform_exists.studybubble.json`
- `topics\terraform_1000_foot_view.studybubble.json`
- `topics\terraform_core_workflow.studybubble.json`
- `topics\terraform_state_drift_backends.studybubble.json`
- `topics\terraform_providers_resources.studybubble.json`

### Existing layouts
- `layouts\iac_why_terraform_exists.layout.json`
- `layouts\terraform_1000_foot_view.layout.json`
- `layouts\terraform_core_workflow.layout.json`
- `layouts\terraform_state_drift_backends.layout.json`
- `layouts\terraform_providers_resources.layout.json`

### Existing outputs
- `outputs\iac_why_terraform_exists.html`
- `outputs\terraform_1000_foot_view.html`
- `outputs\terraform_core_workflow.html`
- `outputs\terraform_state_drift_backends.html`
- `outputs\terraform_providers_resources.html`

### Existing assets
- `assets\iac_landscape_overview.svg`
- `assets\terraform_core_workflow.svg`
- `assets\terraform_state_drift_backends.svg`
- `assets\terraform_providers_resources.svg`

### Tutorials root status
- `D:\Workarea\StudyBook\tutorials\IaC\TerraForm` exists.
- `study_pages\` and `labs\` placeholder structure exists.
- Existing deep page found: `study_pages\03_core_workflow\index.html`.

## 2) Map-by-map audit and retrofit targets

### A) `iac_why_terraform_exists`
- Topic id: `iac_why_terraform_exists`
- Source JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\iac_why_terraform_exists.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\iac_why_terraform_exists.html`
- Image asset: yes (`iac_landscape_overview.svg`)
- childTopics navigation: yes
- mapResources: no
- Notes richness: **thin-medium** (mostly concise, limited deep cards)
- Likely tutorial/lab resource needed:
  - map-level tutorial page: yes
  - hands-on lab: no (conceptual map)
- Suggested tutorial path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\00_iac_why_terraform_exists\index.html`
- Suggested lab path:
  - none for now
- Suggested prompt file path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\00_iac_why_terraform_exists\prompts\recreate_tutorial.md`

### B) `terraform_1000_foot_view`
- Topic id: `terraform_1000_foot_view`
- Source JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_1000_foot_view.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_1000_foot_view.html`
- Image asset: no dedicated note.image currently
- childTopics navigation: yes (multiple)
- mapResources: no
- Notes richness: **thin** (few/no note summaries, heavily navigation-driven)
- Likely tutorial/lab resource needed:
  - map-level tutorial page: yes
  - map-level lab links: yes (to downstream labs, once ready)
- Suggested tutorial path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\01_terraform_1000_foot_view\index.html`
- Suggested lab path:
  - map-level links to `02_core_workflow`, `03_state_drift_backends`, `04_providers_resources`
- Suggested prompt file path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\01_terraform_1000_foot_view\prompts\recreate_tutorial.md`

### C) `terraform_core_workflow`
- Topic id: `terraform_core_workflow`
- Source JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_core_workflow.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_core_workflow.html`
- Image asset: yes (`terraform_core_workflow.svg`)
- childTopics navigation: yes
- mapResources: **yes** (already present)
- Notes richness: **rich**
- Likely tutorial/lab resource needed:
  - map-level tutorial page: yes (already created under `study_pages\03_core_workflow\index.html`)
  - hands-on lab: yes (future, local-safe first)
- Suggested tutorial path:
  - keep current: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\study_pages\03_core_workflow\index.html`
  - optionally converge later to canonical numbered root: `...\02_core_workflow\index.html`
- Suggested lab path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\01_core_workflow\`
- Suggested prompt file path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\01_core_workflow\prompts\create_lab.md`
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\01_core_workflow\prompts\recreate_tutorial.md`

### D) `terraform_state_drift_backends`
- Topic id: `terraform_state_drift_backends`
- Source JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_state_drift_backends.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_state_drift_backends.html`
- Image asset: yes (`terraform_state_drift_backends.svg`)
- childTopics navigation: yes
- mapResources: no
- Notes richness: **rich**
- Likely tutorial/lab resource needed:
  - map-level tutorial page: yes
  - hands-on lab: yes (state/drift demonstrations)
- Suggested tutorial path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\03_state_drift_backends\index.html`
- Suggested lab path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\02_state_drift_backend\`
- Suggested prompt file path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\02_state_drift_backend\prompts\create_lab.md`
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\02_state_drift_backend\prompts\recreate_tutorial.md`

### E) `terraform_providers_resources`
- Topic id: `terraform_providers_resources`
- Source JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_providers_resources.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_providers_resources.html`
- Image asset: yes (`terraform_providers_resources.svg`)
- childTopics navigation: yes
- mapResources: no
- Notes richness: **rich**
- Likely tutorial/lab resource needed:
  - map-level tutorial page: yes
  - hands-on lab: yes (provider/resource identity and references)
- Suggested tutorial path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\04_providers_resources\index.html`
- Suggested lab path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\03_providers_resources\`
- Suggested prompt file path:
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\03_providers_resources\prompts\create_lab.md`
  - `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\labs\03_providers_resources\prompts\recreate_tutorial.md`

## 3) Major gaps found

1. `mapResources` adoption is inconsistent.
- Only `terraform_core_workflow` appears to use top-level mapResources.
- Other maps still depend mostly on bubble-level links/childTopics.

2. Deep study pages exist only for one map.
- `03_core_workflow/index.html` exists; others are placeholders.

3. Lab guide layer is not implemented yet.
- `labs\` has placeholders only; no README/index/lab scripts per module.

4. Bubble card depth is uneven.
- `terraform_1000_foot_view` is thin vs other maps.

5. Canonical tutorial naming split.
- Current deep-page location (`study_pages\03_core_workflow`) differs from desired future numbered map-level tutorial roots (`02_core_workflow`, etc.).

## 4) Proposed mapResources retrofit (per map)

- `iac_why_terraform_exists`
  - Add mapResources: full tutorial, next map (`terraform_1000_foot_view`), glossary/checklist links when created.

- `terraform_1000_foot_view`
  - Add mapResources: overview tutorial page, links to downstream map tutorials/labs (core workflow, state, providers), and “next recommended map”.

- `terraform_core_workflow`
  - Validate/normalize existing mapResources:
    - deep study page link
    - lab README/index targets (once created)
    - back/next map links
    - setup/checklist links

- `terraform_state_drift_backends`
  - Add mapResources: deep tutorial page, backend safety checklist, optional lab guide, sibling link to core workflow.

- `terraform_providers_resources`
  - Add mapResources: deep tutorial page, optional provider/resource lab guide, sibling link back to 1000-foot and forward to modules/variables map when exists.

## 5) Proposed tutorial/lab folder usage against desired structure

Use desired structure as canonical target for new content:
- `...\00_iac_why_terraform_exists\`
- `...\01_terraform_1000_foot_view\`
- `...\02_core_workflow\`
- `...\03_state_drift_backends\`
- `...\04_providers_resources\`

And labs:
- `...\labs\01_core_workflow\`
- `...\labs\02_state_drift_backend\`
- `...\labs\03_providers_resources\`
- `...\labs\04_variables_outputs_locals\`
- `...\labs\05_modules_reuse\`
- `...\labs\06_team_safety_cicd\`
- `...\labs\07_aws_observability_bridge\`

## 6) Recommended first implementation batch

Batch 1 (small, high impact):
1. Add/normalize mapResources in **all five existing maps** using existing paths only.
2. Retrofit `terraform_1000_foot_view` card depth (selected nodes) to medium richness with concise note summaries.
3. Create deep study pages for:
   - `00_iac_why_terraform_exists\index.html`
   - `01_terraform_1000_foot_view\index.html`
4. For `02_core_workflow`, decide canonical strategy:
   - either keep `study_pages\03_core_workflow` as canonical, or
   - migrate to `02_core_workflow` and update links consistently.

Batch 2:
1. Create tutorial pages for state/providers maps.
2. Create lab guide READMEs and prompts only (no cloud apply).
3. Add local-safe examples first; mark AWS apply as optional.

## 7) Risks and unknowns

- Potential link drift if both `study_pages\03_core_workflow` and `02_core_workflow` remain active.
- `mapResources` viewer behavior should be verified in current output UI for non-selected and selected states.
- Lab content must remain local-safe by default; AWS live examples should be optional and approval-gated.

## 8) Engine work needed?

- No immediate engine work indicated by this audit.
- Escalate only if `mapResources` fail to render/navigate as intended in viewer behavior.
