# AGENTS.md

## Project
ServiceCall AI / RAG Demo Workspace

## Root Purpose
This repository is a learning-first and deployment-minded project for building a production-style RAG and AI intake assistant for home-service businesses.

The project has two lanes:
- `pocs/` for small isolated proof-of-concepts
- `integrated/servicecall-ai/` for the assembled solution

## Agent Role
Codex acts as a junior implementation assistant.
Codex is not the product architect.

Codex should:
- work in small slices
- follow project rules
- update project state files
- validate work
- report clearly

Codex should not:
- build the whole app at once
- skip tests
- skip documentation
- move code into integrated/ before it is understood in pocs/
- change architecture direction without approval

## Required Engineering Rules
1. Use Pydantic for all structured inputs, outputs, configs, logs, and AI responses.
2. Use type hints.
3. Use synthetic data only.
4. Every POC must have a README.
5. Every feature must have validation or test coverage.
6. Every supported answer must include citations or fallback.
7. Every risky case must produce escalation logic.
8. Every chat interaction must produce an outcome event.
9. Every AWS resource must have cleanup notes or script.
10. Nothing moves into `integrated/servicecall-ai/` until understood in `pocs/`.

## POC Documentation Standard (Standing Rule)
Every meaningful POC should include:
- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`
- `src/`
- `tests/`
- `outputs/`

## Design-First POC Rule (Standing Rule)
Every meaningful POC, feature, or project step must start with documentation before implementation.

Required documentation deliverables:
- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`

Required implementation deliverables when code is approved:
- `src/`
- `tests/`
- `outputs/`

Important behavior rules:
- Do not implement code before design docs unless explicitly approved.
- Do not skip documentation for small but meaningful POCs.
- Keep documentation teaching-friendly and industry-style.
- Explain why the design exists, not only what files changed.
- Keep each POC standalone, configurable, reusable, and chainable.
- Do not jump ahead to `integrated/servicecall-ai` until the POC ladder supports it.

## POC Acceptance Rule (Standing Rule)
A POC is not complete until:
- `README.md` explains purpose, usage, inputs, outputs, and non-goals
- `docs/DESIGN.md` explains problem, architecture, design decisions, boundaries, and future handoff
- `docs/CONTRACT.md` defines input artifacts, output artifacts, data models, schemas, and required fields
- `docs/TEST_PLAN.md` defines validation strategy, unit tests, integration checks, and acceptance checks
- code exists only after design approval
- tests pass
- sample output exists when the POC produces artifacts
- project tracking/control files are updated

## Environment Bootstrap
Before running Python, pytest, pip, FastAPI, or project scripts, Codex must run:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1
```

## Required Files to Read Before Work
1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `TASK_BOARD.md`
4. `HANDOFF.md`
5. `DECISIONS.md`
6. `KNOWN_ISSUES.md`

## Required Files to Update After Work
1. `PROJECT_STATE.md`
2. `TASK_BOARD.md`
3. `DAILY_LOG.md`
4. `HANDOFF.md`
5. `CHANGELOG.md` when structure or behavior changes
6. `DECISIONS.md` when an architecture/product decision is made
7. `KNOWN_ISSUES.md` when a bug, blocker, or risk is found

## Closed-Loop Reporting
After every task, return:

### A) Task Status Report
- changed files
- what was done
- validation performed
- pass/fail
- open issues
- next recommended task

### B) Project Condition Summary
- current milestone
- current lane
- what works now
- what is still missing
- current risks
- files updated for project memory

## Stop Rule
If a request expands beyond the current milestone, stop and ask before proceeding.

Examples:
- building backend during static website milestone
- touching `integrated/` during POC milestone
- adding AWS resources before cleanup exists
- using real business/customer data
- skipping tests or documentation
