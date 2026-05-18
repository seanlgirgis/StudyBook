# Terraform Variables, Outputs, and Locals Lab

## Purpose
This local-safe lab teaches how Terraform accepts inputs, computes reusable internal values, and exposes useful outputs.

## What This Lab Teaches
- variables as inputs
- variable types and defaults
- tfvars usage
- sensitive values
- locals for internal reuse
- outputs for sharing values
- environment-specific input patterns
- reuse pattern and plan impact

## Files Included
- main.tf
- ariables.tf
- 	erraform.tfvars.example
- dev.tfvars.example
- prod.tfvars.example
- outputs.tf
- xpected_output/*
- prompts/*
- 	roubleshooting.md
- index.html

## Prerequisites
- Terraform CLI 1.4+ recommended
- Local terminal access

## Safety Note
No AWS credentials are required. No cloud resources are created. 	erraform apply is intentionally not part of this first safe lab.

## Setup Steps
1. Open a terminal in this folder.
2. Run init/check/plan commands.
3. Compare default vs dev/prod tfvars plans conceptually.

## Commands To Run
`powershell
terraform version
terraform init
terraform fmt
terraform validate
terraform plan
terraform plan -var-file="dev.tfvars.example"
terraform plan -var-file="prod.tfvars.example"
`

## What To Notice
- variables define configurable inputs
- tfvars swaps environment values without changing core logic
- locals compose reusable internal values
- outputs expose useful values for people/automation
- plan reflects different inputs while keeping same pattern

## Expected Outputs
See xpected_output/ notes for conceptual interpretation.

## Variables
Variables are external inputs used by resources and locals.

## tfvars
tfvars files provide environment-specific values so core code remains reusable.

## Locals
Locals are internal computed values for naming/tagging/repeated expressions.

## Outputs
Outputs expose final values, including structured objects from local-safe resources.

## Environment Inputs
dev.tfvars.example and prod.tfvars.example demonstrate same reusable pattern with different values.

## Cleanup Notes
No cloud resources are created in this lab. You can remove .terraform/ locally for reset.

## Connection Back to StudyBubble Maps
- 	erraform_variables_outputs_locals
- 	erraform_core_workflow
- 	erraform_state_drift_backends
- 	erraform_providers_resources

## Optional Next Steps
- Convert this pattern into a module-focused map/lab
- Add safe policy checks and validation conventions
