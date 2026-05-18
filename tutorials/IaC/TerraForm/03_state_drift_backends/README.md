# Terraform State, Drift, and Backends Lab

## Purpose
This local-safe lab teaches Terraform state concepts without creating cloud resources.

## What This Lab Teaches
- what Terraform state is and why it exists
- how state maps configuration to managed objects
- why local state is fine for learning but risky for teams
- what remote backends and locking are for
- why state may be sensitive
- what drift means and how plan can reveal it
- what import and state commands mean conceptually
- common state mistakes to avoid

## Files Included
- main.tf
- ackend_notes.md
- xpected_output/*
- prompts/*
- 	roubleshooting.md
- index.html

## Prerequisites
- Terraform CLI 1.4+ recommended
- Local terminal access

## Safety Note
No AWS credentials, no cloud resources, no paid services, and no 	erraform apply required.

## Plan-Focused Scope
- plan shows what Terraform would do
- state details are most visible after apply
- this run intentionally stops before apply

## Setup Steps
1. Open terminal in this folder.
2. Run init/validate/plan commands.

## Commands To Run
`powershell
terraform version
terraform init
terraform validate
terraform plan
`

## What To Notice
- version confirms tooling
- init prepares local working directory
- validate checks structure
- plan previews local-safe 	erraform_data change

## Expected Outputs
Read files under xpected_output/.

## Local State Explanation
Local state is fine for learning, but team workflows usually require remote state.

## Remote Backend Explanation
Backends control where state lives. Teams use remote backends for shared truth and controls.

## Locking Explanation
Locking prevents concurrent writes to state.

## Drift Explanation
Drift is mismatch caused by changes outside Terraform. Plan can reveal this mismatch.

## Cleanup Notes
No cloud resources are created. You can delete .terraform/ to reset local metadata.

## Connection Back to StudyBubble Map
This supports 	erraform_state_drift_backends.

## Optional Next Steps
- Add an approved local-only apply variant in a separate lab.
