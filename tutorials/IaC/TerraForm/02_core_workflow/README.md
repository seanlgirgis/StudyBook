# Terraform Core Workflow Lab

## Purpose

This is a local-safe Terraform tutorial/lab package for understanding the core workflow without creating cloud resources.

## What this lab teaches

- what `.tf` files are
- `terraform init`
- `terraform fmt`
- `terraform validate`
- `terraform plan`
- human plan review thinking
- why `apply` is powerful
- why `destroy` is risky

## Files included

- `README.md`
- `index.html`
- `main.tf`
- `variables.tf`
- `outputs.tf`
- `expected_output/`
- `prompts/`
- `troubleshooting.md`

## Prerequisites

- Terraform CLI recommended (`>= 1.4.0`)
- Local terminal (PowerShell is fine)

## Safety note

This lab is local-safe:
- no AWS credentials required
- no cloud provider required
- no paid resources
- `terraform apply` is intentionally not part of this first lab

## Setup steps

1. Open a terminal in this folder.
2. Confirm Terraform is available.
3. Run init/fmt/validate/plan in order.

## Commands to run

```powershell
terraform version
terraform init
terraform fmt
terraform validate
terraform plan
```

## What to notice after each command

- `version`: confirms Terraform is installed and version compatibility.
- `init`: prepares local working directory and provider components.
- `fmt`: enforces canonical Terraform formatting.
- `validate`: checks configuration structure and syntax.
- `plan`: previews intended changes before any execution.

## Expected outputs

See files under `expected_output/`:
- `terraform_version.txt`
- `terraform_fmt.txt`
- `terraform_validate.txt`
- `terraform_plan_notes.txt`

## Cleanup notes

No cloud resources are created in this lab design.
Local working artifacts like `.terraform/` and `.terraform.lock.hcl` may be created by `init`.

## Connection back to StudyBubble map

This lab supports the map:

`D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\terraform_core_workflow.html`

It gives practical context for bubbles such as Write Configuration, Initialize, Format, Validate, Plan, Review Plan, Apply, and Outputs.

## Optional next steps

- Add variable overrides and inspect plan diffs.
- Add a second `terraform_data` block and observe dependency behavior.
- Progress to state/backends map and then provider/resource map.
