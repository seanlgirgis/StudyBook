# Terraform Safety, Team Workflow, and CI/CD Lab

## Purpose
This local-safe lab teaches how Terraform safety works as a team change-management process, not just a set of commands.

## What This Lab Teaches
- Terraform as team change management
- version control and pull request flow
- terraform fmt and validate checks
- plan review and blast radius review
- controlled apply concepts
- remote state and locking concepts
- least privilege
- CI/CD workflow shape
- policy checks
- rollback thinking
- production approval gates
- safe interview wording

## Files Included
- `main.tf`
- `variables.tf`
- `outputs.tf`
- `pr_checklist.md`
- `plan_review_checklist.md`
- `blast_radius_checklist.md`
- `apply_control_runbook.md`
- `cicd_pipeline_pseudocode.yml`
- `policy_check_examples.md`
- `rollback_notes.md`
- `expected_output/`
- `prompts/`
- `troubleshooting.md`

## Prerequisites
- Terraform CLI 1.4+ (optional for reading, needed for command practice)
- Local terminal access

## Safety Note
- No AWS credentials required.
- No cloud resources created.
- No real cloud provider required.
- `terraform apply` is intentionally excluded.
- CI/CD examples are pseudo/workflow examples only.
- No real backend is configured.
- No real infrastructure is changed.

## Setup Steps
1. Open this folder in your terminal.
2. Review `main.tf`, `variables.tf`, and `outputs.tf`.
3. Read the checklist and runbook markdown files.
4. Review pseudo-pipeline and policy examples.

## Commands To Run
```powershell
terraform version
terraform fmt
terraform validate
terraform plan
```

## What To Notice After Each Command
- `version`: confirms Terraform CLI is available.
- `fmt`: standardizes formatting and may report changed files.
- `validate`: checks config structure and syntax.
- `plan`: previews local-safe change metadata and outputs.

## Expected Outputs
See the `expected_output/` files for conceptual guidance.

## Version Control
Version control provides history, traceability, and review discipline for infrastructure code.

## Pull Request
PR review adds human and process checkpoints before any apply path is considered.

## Format/Validate
These are early quality checks; they do not replace plan review or approvals.

## Plan Review
Plan review is the key safety checkpoint for intended create/change/destroy behavior.

## Blast Radius
Blast radius review checks impact scope before approving real changes.

## Apply Control
Apply should be controlled by role, environment, and approval gates; not casual laptop-to-prod use.

## Remote State and Locking
Remote state and locking are team safety controls for shared infrastructure management.

## Least Privilege
Credentials should be scoped to minimum required permissions.

## CI/CD
CI/CD should standardize checks and review evidence; apply remains gated.

## Policy Checks
Policy checks provide repeatable guardrails for tagging, security, and compliance expectations.

## Rollback Thinking
Rollback must be planned; infrastructure recovery is not always a simple code revert.

## Pre-Apply Safety Checklist
- right branch?
- right pull request?
- right environment?
- right workspace?
- right backend/state?
- right credentials?
- right approval?
- plan reviewed?
- destroy/replacement checked?
- rollback path understood?

## Connect Back To StudyBubble
- [Terraform Safety, Team Workflow, and CI/CD](../../../../study_maps/IaC/TerraForm/outputs/terraform_safety_team_workflow_cicd.html)
- [Terraform Environments and Workspaces](../../../../study_maps/IaC/TerraForm/outputs/terraform_environments_workspaces.html)
- [Terraform State, Drift, and Backends](../../../../study_maps/IaC/TerraForm/outputs/terraform_state_drift_backends.html)
- [Terraform Core Workflow](../../../../study_maps/IaC/TerraForm/outputs/terraform_core_workflow.html)

## Optional Next Steps
1. Practice safer plan-review wording with your team.
2. Extend this into a local-only mock approval workflow.
3. Continue to AWS, Observability, and Interview Bridge once that map is added.
