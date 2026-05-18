# Backend Strategy Notes

## What backend per environment means
Backend per environment means state for dev, test, and prod is stored in separate backend locations or state paths.

## Why state boundaries should match environment boundaries
If environments share state carelessly, a change intended for one environment can affect another. Separate state boundaries reduce this risk.

## Why this lab does not configure a real backend
This is a safe local lab focused on concepts. It avoids real backend setup, cloud storage, and credentials.

## Backend is not the same as workspace
- Backend: where state is stored.
- Workspace: named state instances within a configuration context.

## Backend is not the same as provider
- Backend handles Terraform state storage.
- Provider talks to external APIs/resources.

## Conceptual examples
- dev state path: `terraform/dev/learnterraform.tfstate`
- test state path: `terraform/test/learnterraform.tfstate`
- prod state path: `terraform/prod/learnterraform.tfstate`

## Warning
This lab does not configure a real remote backend. Do not copy backend examples into real use without approved storage, locking, encryption, and access control.
