# Troubleshooting

## terraform command not found
Terraform CLI is not installed or not on PATH. Install Terraform and reopen the terminal.

## unsupported Terraform version
This lab expects Terraform 1.4+ due to local-safe resource usage.

## fmt changed files
That is normal. `terraform fmt` standardizes file formatting.

## validate failure
Read the error line and file path. Check syntax, braces, and variable names.

## tfvars file not found
Run from the lab folder and use exact filenames:
- dev.tfvars.example
- test.tfvars.example
- prod.tfvars.example

## plan output looks unfamiliar
Focus on conceptual differences in environment input values. Exact output formatting varies by Terraform version.

## confusion between tfvars and workspace
- tfvars: value inputs.
- workspace: selected state instance.

## confusion between workspace and backend
- workspace: named state instance.
- backend: where state is stored.

## wrong environment fear
Use pre-change checklist: folder, var-file, workspace, backend path, account, approval.

## accidental apply concern
This lab does not require apply. Stop and verify context before any real apply in other workflows.

## cleanup guidance
No resources are created because apply is not run.
