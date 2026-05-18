# LearnTerraform Curriculum State

## Purpose

This file preserves the learning design for the LearnTerraform study project.

It is not a StudyBubble engine/process file.

It does not explain how to build, sync, export, or run StudyBubble.

It explains what Terraform material we decided to study, why it matters, how
the maps connect, and how the learning should progress.

The goal is to learn Terraform through small connected bubble maps that build
interview fluency and real practical understanding.

---

## 1. Learning Mission

LearnTerraform helps Sean build Terraform fluency for:

- cloud infrastructure conversations
- infrastructure-as-code understanding
- AWS-facing data engineering work
- observability and platform engineering interviews
- capacity engineering modernization
- safe technical storytelling
- collaboration with DevOps, cloud, SRE, and platform teams

This project is not meant to turn Sean into a fake Terraform production owner.

The intended outcome is:

```text
Sean can explain what Terraform does, how the workflow works, why state matters,
how teams use it safely, and how it connects to AWS, observability, and cloud
platform work.
```

Map -1: IaC: Why Terraform Exists
Topic ID: iac_why_terraform_exists
Purpose: explain the IaC landscape, Terraform alternatives, and why Terraform became important before studying Terraform internals.


Map 2: Terraform Core Workflow
Topic ID: terraform_core_workflow
Purpose: teach the practical Terraform lifecycle from writing configuration through init, fmt, validate, plan, review, apply, outputs, ongoing changes, and destroy safety.


Map 6: Terraform State, Drift, and Backends
Topic ID: terraform_state_drift_backends
Purpose: teach why state matters, how Terraform maps configuration to real infrastructure, how drift happens, and why remote backends, locking, and careful state operations protect teams.


Map 4: Terraform Providers and Resources
Topic ID: terraform_providers_resources
Purpose: teach how providers connect Terraform to platforms and how resources describe the infrastructure objects Terraform manages.

