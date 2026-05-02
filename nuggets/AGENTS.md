# AGENTS.md — Nuggets Repository Constitution

## Purpose

This repository is a learning scratchbook for small IT experiments, examples, and practice ideas.

It is not a polished tutorial repo. It is a safe place to test concepts quickly in Python, data engineering, AWS, testing, architecture, and related topics.

## Phase Discipline

This repository starts with a phase-1 scaffold only.

Phase 1 files are:

- AGENTS.md
- README.md
- NUGGET_INDEX.md
- RUNBOOK.md

Do not create additional governance files unless the user explicitly asks.

Deferred files include:

- NUGGET_RULES.md
- EXPERIMENT_LOG.md
- LESSONS_LEARNED.md

Create those later only when the repo has enough real nuggets to justify them.

## Environment Rule

All Python work must be run from this repository root:

```powershell
cd D:\Workarea\StudyBook\nuggets
..\env_setter.ps1
```

Use only relative paths inside this repository.

Do not hardcode absolute paths except when documenting this repository root for the user.

## Path Rules

* Use relative paths in code.
* Prefer `Path(__file__).resolve().parent` or paths relative to the script location.
* Do not write outside this repository unless explicitly instructed.
* Do not modify files in parent StudyBook tutorial folders.
* Do not assume access to other repositories.

## Nugget Rules

Each experiment should be small, focused, and runnable.

A nugget should usually include:

* one clear topic
* one runnable script
* optional small test
* short notes explaining what was learned
* clear command to run it

Prefer creating a new folder instead of overwriting existing work.

## Folder Naming

Use descriptive numbered folders when helpful:

```text
python/001_file_paths/
python/002_json_validation/
data_engineering/001_csv_to_parquet/
testing/001_pytest_basics/
aws/001_s3_concepts_mock/
```

## Safety Rules

* Do not create AWS resources unless explicitly asked.
* Prefer local simulations before real cloud calls.
* If AWS code is created, include a cost/safety warning.
* Never store secrets in this repo.
* Never print secrets.
* Use `.env.example`, not `.env`, when showing environment variables.

## Code Quality Rules

* Keep examples simple and readable.
* Prefer standard library first.
* Add comments only where they help learning.
* Scripts should print useful output.
* Tests should be runnable with pytest.
* Avoid large dependencies unless the user asks.

## Testing Rule

When practical, include a tiny pytest test.

Preferred command:

```powershell
python -m pytest
```

## Markdown Quality Rule

All markdown files must have complete, closed code fences.

Never leave a partial code block open.

Before finishing, check that every opening triple-backtick has a matching closing triple-backtick.

## Output Rule

At the end of every Codex task, report:

* files created or changed
* exact commands to run
* expected output
* what the nugget teaches
* any cleanup needed

## Do Not Do

* Do not turn every nugget into a huge framework.
* Do not overwrite existing nuggets unless requested.
* Do not create complex abstractions too early.
* Do not make company-style production code unless asked.
* Do not hide important assumptions.

## Preferred Style

Small. Clear. Runnable. Educational.

Use only relative paths. Never modify parent tutorial folders.
