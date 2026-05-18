# LearnTerraform Foundation Checkpoint V1

## Current Status
The LearnTerraform foundation is now usable as a StudyBubble-based learning system and currently consists of:

- course home page
- 5 StudyBubble maps
- mapResources navigation
- tutorial pages
- local-safe lab guides for workflow/state/providers
- sample Terraform files where appropriate
- expected output notes
- troubleshooting pages
- recreate prompts

## Course Home

Path:

`D:\Workarea\StudyBook\tutorials\IaC\TerraForm\index.html`

## Maps Completed

### 1) iac_why_terraform_exists
- Topic JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\iac_why_terraform_exists.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\iac_why_terraform_exists.html`
- Tutorial: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\00_iac_why_terraform_exists\index.html`
- Lab README: none (orientation/tutorial-only)
- Image asset: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\assets\iac_landscape_overview.svg`

### 2) terraform_1000_foot_view
- Topic JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_1000_foot_view.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_1000_foot_view.html`
- Tutorial: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\01_terraform_1000_foot_view\index.html`
- Lab README: none (orientation/tutorial-only)
- Image asset: none specific to this map source

### 3) terraform_core_workflow
- Topic JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_core_workflow.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_core_workflow.html`
- Tutorial: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\02_core_workflow\index.html`
- Lab README: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\02_core_workflow\README.md`
- Image asset: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\assets\terraform_core_workflow.svg`

### 4) terraform_state_drift_backends
- Topic JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_state_drift_backends.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_state_drift_backends.html`
- Tutorial: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\03_state_drift_backends\index.html`
- Lab README: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\03_state_drift_backends\README.md`
- Image asset: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\assets\terraform_state_drift_backends.svg`

### 5) terraform_providers_resources
- Topic JSON: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\topics\terraform_providers_resources.studybubble.json`
- Generated HTML: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_providers_resources.html`
- Tutorial: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\04_providers_resources\index.html`
- Lab README: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\04_providers_resources\README.md`
- Image asset: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\assets\terraform_providers_resources.svg`

## Browser Acceptance
Sean confirmed:

- course home/index opens and is useful
- mapResources stay visible no matter which bubble is selected
- tutorial links open
- Core Workflow tutorial works
- State/Drift/Backends tutorial works
- Providers/Resources tutorial works

## Current Design Law

- Map first, then teach from the map
- Bubble cards should teach enough, not just slogans
- Images should be used when helpful
- mapResources are for whole-map/course resources
- childTopics are for concept-specific map jumps
- tutorials/labs live under `tutorials/`
- no generated HTML hand editing
- no StudyBubble engine work unless something breaks

## Safety Rules

- no AWS credentials assumed
- no cloud resources created
- no `terraform apply` in current safe labs
- AWS snippets are conceptual unless explicitly approved
- Sean should not overclaim Terraform production ownership

## Next Recommended Content Map

Next map candidate:

`terraform_variables_outputs_locals`

Purpose:
Teach variables, variable types, defaults, tfvars, sensitive values, locals, outputs, naming patterns, and environment inputs.

## Next Recommended Tutorial/Lab Direction

After the variables map is created and accepted, create a local-safe tutorial and lab package for it.

## Known Watch Items

- targeted `bubbles build <topic>` may be needed because full build may not refresh all maps in this setup
- mapResources work in browser as currently observed
- check relative links whenever creating tutorial pages
- continue using `.studybubble.json` references for topic navigation

- Planned mapResources should not point to missing files.
- Future planned tutorial/lab links require placeholder pages or should be omitted until active.

