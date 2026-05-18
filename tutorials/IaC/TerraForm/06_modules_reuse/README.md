# Terraform Modules and Reuse Lab

## Purpose
This local-safe lab teaches how Terraform modules package reusable patterns and return standardized values.

## What This Lab Teaches
- what a module is
- root module vs child module
- module inputs and outputs
- local module source paths
- reuse and standards
- versioning mindset and module risk
- how modules build on variables and outputs

## Files Included
- `main.tf`
- `variables.tf`
- `outputs.tf`
- `modules/naming_standard/main.tf`
- `modules/naming_standard/variables.tf`
- `modules/naming_standard/outputs.tf`
- `expected_output/*`
- `prompts/*`
- `troubleshooting.md`
- `index.html`

## Prerequisites
- Terraform CLI 1.4+ recommended
- local terminal access

## Safety Note
No AWS credentials required. No cloud resources. No `terraform apply` in this safe lab.

## Setup Steps
1. Open terminal in this folder.
2. Run init/fmt/validate/plan.
3. Review how root and child module values flow.

## Commands to Run
```powershell
terraform version
terraform init
terraform fmt
terraform validate
terraform plan
```

## What to Notice
- root module calls child module via local source
- root passes inputs to child module
- child returns outputs to root
- root uses module outputs in local-safe `terraform_data`

## Expected Outputs
See `expected_output/` notes.

## Root Module
The root module is the current working directory where Terraform runs.

## Child Module
The child module lives under `modules/naming_standard` and defines reusable naming/tagging logic.

## Module Inputs
Inputs are variables passed from root into child module.

## Module Outputs
Outputs return computed values from child module back to root module.

## Local Module Source
This lab uses local source path: `./modules/naming_standard`.

## Reuse and Standards
Modules help teams reuse patterns for naming, tagging, and consistency.

## Module Risks
Overly complex modules, unclear outputs, and weak review/version discipline can spread risk.

## Cleanup Notes
No cloud resources are created. Remove `.terraform/` locally if needed.

## Connection Back to StudyBubble Map
- `terraform_modules_reuse`
- `terraform_variables_outputs_locals`
- `terraform_core_workflow`
- `terraform_providers_resources`

## Optional Next Steps
- add controlled version pinning examples
- expand to module registry/Git source patterns in a future approved lab
