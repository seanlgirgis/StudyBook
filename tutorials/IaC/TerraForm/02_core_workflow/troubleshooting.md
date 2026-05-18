# Troubleshooting — Terraform Core Workflow Lab

## terraform command not found
- Terraform CLI is not installed or not on PATH.
- Install Terraform and reopen terminal.

## Unsupported Terraform version
- This lab expects Terraform >= 1.4.0 for `terraform_data`.
- Run `terraform version` and upgrade if needed.

## init confusion
- Run commands from `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\02_core_workflow`.
- `terraform init` prepares local working metadata.

## fmt changed files
- This is normal. `terraform fmt` rewrites style to canonical formatting.

## validate failure
- Check syntax in `main.tf`, `variables.tf`, and `outputs.tf`.
- Re-run `terraform fmt` then `terraform validate`.

## plan output looks unfamiliar
- Focus on high-level action summary and reviewed intent.
- This lab is local-safe and should stay simple.

## accidental apply concern
- This run intentionally does not use apply.
- If apply was run by accident, stop and inspect state before further steps.

## cleanup guidance
- No cloud resources are created by design in this lab.
- Local artifacts can be removed if needed (`.terraform/`, lock file) after learning.
