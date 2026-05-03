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

## 2026-05-03 - Adopt Standard POC Documentation and Completion Gate
### Decision
Adopt a standing POC standard requiring each meaningful POC to include:
- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`
- `src/`
- `tests/`
- `outputs/`

Adopt a standing acceptance gate: a POC is not complete until code works, tests pass, sample output exists, and the four documentation files are complete.

### Why
This preserves consistency across POCs, improves handoff quality, and prevents implementation-only closure without clear architecture, contracts, and validation intent.

### Scope
Applies to all current and future meaningful POCs in this repository unless explicitly superseded.

## 2026-05-03 - Adopt Design-First POC Rule
### Decision
Adopt a standing design-first rule for every meaningful POC, feature, or project step:
- documentation must come before implementation (`README`, `docs/DESIGN.md`, `docs/CONTRACT.md`, `docs/TEST_PLAN.md`)
- implementation deliverables are required only after code approval (`src/`, `tests/`, `outputs/`)
- POC acceptance requires complete docs, passing tests, sample output (when applicable), and updated tracking files

### Why
This improves architecture clarity, teaching quality, reviewability, and implementation discipline while preventing rushed code-first drift.

### Scope
Applies to all meaningful POCs/features/steps in this repository unless explicitly superseded.
