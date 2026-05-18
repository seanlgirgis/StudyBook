# Terraform Providers and Resources Lab

## Purpose
This is a local-safe concept lab for learning providers and resources without cloud execution.

## What This Lab Teaches
- what a provider is
- AWS provider conceptually
- provider configuration and version constraints
- resource type vs name vs address
- attributes, data sources, dependencies
- provider vs backend

## Files Included
- main.tf
- versions.tf
- providers.tf
- expected_output/*
- prompts/*
- troubleshooting.md
- index.html

## Prerequisites
- Terraform CLI 1.4+ recommended

## Safety Note
No AWS credentials, no cloud resources, no apply required.

## Local-Safe Scope
This lab uses terraform_data only. AWS snippets are conceptual only and not executed.

## Setup Steps
1. Open terminal in this folder.
2. Run version/init/validate/plan.

## Commands
`powershell
terraform version
terraform init
terraform validate
terraform plan
`

## What To Notice
- Provider concept vs resource concept
- Resource address shape: 	ype.name
- Attributes can be referenced between resources
- References create dependency order

## Expected Outputs
See files under xpected_output/.

## Provider vs Backend
Provider talks to platform APIs. Backend stores Terraform state.

## Resource Type/Name/Address
- Type = kind of object
- Name = local Terraform identifier
- Address = 	ype.name

## Attributes and Dependencies
Referenced attributes create implicit dependencies.

## Cleanup Notes
No cloud resources are created. Remove .terraform/ to reset local metadata.

## StudyBubble Connection
Supports map: 	erraform_providers_resources.

## Optional Next Steps
Optional AWS lab can be added only after approval, credentials, cost controls, and cleanup plan.
