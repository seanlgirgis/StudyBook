# DECISIONS.md

## 2026-05-01 - Adopt Closed-Loop Project-Control Protocol
### Decision
Adopt a permanent closed-loop protocol requiring:
- explicit startup file reads
- explicit after-task memory updates
- structured task report and project condition summary
- milestone stop-rule escalation before out-of-scope expansion

### Why
This keeps progress auditable, reduces drift, and protects milestone discipline while the project is still in foundational POC stages.

### Scope
Applies to all tasks in this repository until superseded by a newer documented decision.
