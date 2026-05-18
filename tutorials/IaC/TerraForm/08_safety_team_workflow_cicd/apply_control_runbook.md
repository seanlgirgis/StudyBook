# Apply Control Runbook

## Who may apply
Only approved roles or approved CI identities.

## Where apply should run
Controlled CI/CD context, not casual local production applies.

## Approval requirements
Production requires explicit human approval and documented plan review.

## Branch/tag expectations
Use approved branch and merge strategy before apply.

## State lock expectations
Confirm lock behavior and no concurrent active run.

## Logs/artifacts to keep
Keep plan output, approval record, pipeline logs, and post-check evidence.

## Emergency stop condition
Stop if environment, state, workspace, or plan scope is unclear.

## Post-apply verification
Verify expected resources, outputs, and monitoring signals.

## Reminder
No laptop-to-prod as casual default.
