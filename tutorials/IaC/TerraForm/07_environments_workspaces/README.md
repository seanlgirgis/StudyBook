# Terraform Environments and Workspaces Lab

## Purpose
This local-safe lab teaches how the same Terraform pattern can be planned across dev, test, and prod using different inputs, while keeping safety boundaries clear.

## What This Lab Teaches
- what an environment is
- environment separation
- folder strategy
- variable strategy
- tfvars per environment
- workspaces and workspace caution
- backend-per-environment concept
- promotion from dev to test to prod
- wrong-environment risk
- how environments build on variables/modules/state

## Files Included
- `main.tf`
- `variables.tf`
- `outputs.tf`
- `dev.tfvars.example`
- `test.tfvars.example`
- `prod.tfvars.example`
- `backend_strategy_notes.md`
- `workspace_notes.md`
- `expected_output/`
- `prompts/`
- `troubleshooting.md`

## Prerequisites
- Terraform CLI 1.4+ (optional for reading, needed for command practice)
- Local terminal access

## Safety Note
- No AWS credentials required.
- No cloud resources are created.
- No real cloud provider is required.
- `terraform apply` is intentionally not part of this lab.
- Do not configure a real remote backend in this lab.

## Setup Steps
1. Open this folder in a terminal.
2. Review `main.tf`, `variables.tf`, and tfvars files.
3. Review `backend_strategy_notes.md` and `workspace_notes.md` before planning.

## Commands To Run
```powershell
terraform version
terraform init
terraform fmt
terraform validate
terraform plan -var-file="dev.tfvars.example"
terraform plan -var-file="test.tfvars.example"
terraform plan -var-file="prod.tfvars.example"
```

## What To Notice
- `init` prepares local working state for this configuration.
- `fmt` normalizes file formatting.
- `validate` checks Terraform syntax and config structure.
- each `plan` shows different environment values while staying local-safe.

## Expected Outputs
See `expected_output/` for conceptual notes by command and environment.

## Environment Separation
Environment separation means dev, test, and prod are treated as distinct contexts with distinct risk and review needs.

## tfvars Per Environment
Each tfvars file supplies different values while reusing the same Terraform configuration.

## Folder Strategy
Folder boundaries help humans and pipelines see what environment context they are operating in.

## Workspaces and Caution
Workspaces can isolate state instances, but teams must confirm active workspace before planning or applying.

## Backend Per Environment Concept
Backend boundaries should align with environment boundaries. This lab explains the concept only; it does not configure a real backend.

## Promotion Path
Safe change flow is typically: dev validation -> test validation -> production approval and controlled apply.

## Wrong-Environment Risk
One of the highest Terraform risks is running against the wrong folder/workspace/backend/account.

### Safety Checklist Before Any Real Apply
- right folder?
- right variable file?
- right workspace?
- right backend/state?
- right cloud account?
- right approval?

## Cleanup Notes
No resources are created because `apply` is not run. Cleanup is usually just closing the workspace.

## Connect Back To StudyBubble
- [Terraform Environments and Workspaces map](../../../../study_maps/IaC/TerraForm/outputs/terraform_environments_workspaces.html)
- [Terraform Modules and Reuse map](../../../../study_maps/IaC/TerraForm/outputs/terraform_modules_reuse.html)
- [Terraform Variables, Outputs, and Locals map](../../../../study_maps/IaC/TerraForm/outputs/terraform_variables_outputs_locals.html)
- [Terraform State, Drift, and Backends map](../../../../study_maps/IaC/TerraForm/outputs/terraform_state_drift_backends.html)

## Optional Next Steps
1. Compare plan output differences across dev/test/prod inputs.
2. Discuss which boundaries should be folder-based vs workspace-based in your team.
3. Build the next map: Safety, Team Workflow, and CI/CD.
