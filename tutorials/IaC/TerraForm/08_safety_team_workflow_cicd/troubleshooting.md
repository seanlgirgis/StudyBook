# Troubleshooting

## terraform command not found
Install Terraform CLI or add it to PATH.

## unsupported Terraform version
This lab expects Terraform 1.4+.

## fmt changed files
Normal behavior. Review and keep standardized formatting.

## validate failure
Inspect error line/file and fix syntax or references.

## plan output looks unfamiliar
Output shape varies by version. Focus on conceptual change metadata.

## confusion between validate and plan review
Validate checks configuration structure; plan review checks proposed impact.

## confusion between PR approval and apply approval
PR approval reviews code; apply approval authorizes infrastructure execution.

## confusion between CI/CD and real deployment
This lab uses pseudo-pipeline only; it does not deploy.

## state lock confusion
Locking protects state from concurrent writes in team workflows.

## least privilege confusion
Least privilege means only necessary permissions are granted.

## policy check confusion
Policy examples are conceptual, not a live policy engine.

## rollback misconception
Rollback may need more than code revert due to infrastructure side effects.

## accidental apply concern
Apply is intentionally out of scope here. Stop and verify context before any real apply.

## cleanup guidance
No infrastructure is created because apply is not run.
