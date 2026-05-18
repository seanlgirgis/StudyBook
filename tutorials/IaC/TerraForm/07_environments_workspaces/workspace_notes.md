# Workspace Notes

## What Terraform workspaces are
A workspace is a named state instance for the same Terraform configuration.

## Why workspaces can be useful
They can separate state instances (for example, dev/test/prod style naming) while reusing a single configuration.

## Why workspaces can be dangerous
If someone forgets which workspace is active, plan/apply may target the wrong state instance.

## Why teams may prefer folder/backend separation for production clarity
Folder and backend boundaries are often easier to audit and reason about in team workflows.

## Conceptual commands (not required for this first lab)
- `terraform workspace list`
- `terraform workspace show`
- `terraform workspace new dev`
- `terraform workspace select dev`

Use these only if you choose to experiment locally later. This first lab is plan-focused and does not require workspace operations.
