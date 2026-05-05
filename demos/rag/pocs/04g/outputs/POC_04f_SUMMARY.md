# POC 04f Summary Snapshot (Teaching Reference)

![Deployment Diagram](D:/Workarea/StudyBook/demos/rag/Deployment.png)

## Purpose
This document is the current self-contained teaching snapshot for POC 04f in `demos/rag`.
It explains and evidences the deterministic Docker-first workflow for onboarding, review, extension, and debugging.

## Scope and Core Structure
- Project path: `pocs/04f/`
- Core folders:
  - `src/` for deterministic service and container runtime files
  - `tests/` for in-container pytest endpoint and validation checks
  - `docs/` for design, contract, and test planning
  - `outputs/` for reproducible artifacts and logs
- Automation scripts:
  - `integrate_04f_docker.ps1` (primary Docker-first workflow)
  - `integrate_04f.ps1`
  - `run_04f_integration.ps1`
  - `docker-compose.yaml` (alternate runtime path)

## Deterministic Service Contract
- Endpoints under test:
  - `GET /health`
  - `GET /ping`
- Deterministic response shape for both:
```json
{"ok": true}
```
- Validation behavior also verified:
  - unknown endpoint returns `404`

## Real Endpoint Tests (Placeholder Replaced)
`tests/test_integration.py` now contains real HTTP endpoint tests against the running container service:
- `test_health_endpoint_returns_deterministic_ok`
- `test_ping_endpoint_returns_deterministic_ok`

`tests/test_validation.py` verifies behavior boundary:
- `test_unknown_endpoint_returns_not_found` (expects HTTP `404`)

This replaces prior placeholder-only coverage and gives executable deterministic endpoint assertions.

## Docker-First Execution Flow (Step by Step)
1. Mirror and verify POC folder structure.
2. Load environment (`env_setter.ps1`) for consistent tooling context.
3. Build Docker image from `src/Dockerfile`.
4. Run container in detached mode with fixed mapping (`8000:8000`).
5. Execute pytest inside container against mounted `/workspace/tests`.
6. Run smoke checks for `/health` and `/ping`.
7. Persist logs under `outputs/logs/`.
8. Confirm image/container/port status and evidence paths.

Primary script:
- `pocs/04f/integrate_04f_docker.ps1`

## Flow Summary (Textual Visual)
`Build image` -> `Start container` -> `Run in-container pytest` -> `Run smoke checks` -> `Write logs/artifacts` -> `Teaching snapshot update`

## Runtime Identifiers
- Docker image: `poc_04f_service`
- Container name: `poc_04f_service_run`
- Port mapping: host `8000` -> container `8000`

## Evidence From outputs/
### 1) Pytest results
Source:
- `outputs/logs/test_results.log`

Current snapshot summary:
- `collected 3 items`
- `3 passed`
- `0 failed`

### 2) Smoke test results
Source:
- `outputs/logs/smoke_test.log`

Current snapshot summary:
- overall `ok: true`
- `/health` returns `200` with `{"ok": true}`
- `/ping` returns `200` with `{"ok": true}`

### 3) Example request/response artifacts
Sources:
- `outputs/example_requests.json`
- `outputs/example_responses.json`

Current snapshot summary:
- request catalog includes `/health`, `/ping`, and unknown-route validation example
- response catalog captures deterministic `200` results and `404` boundary expectation

## Reproducibility Notes
- Deterministic endpoints produce stable outputs for identical requests.
- Docker-first execution normalizes runtime differences across machines.
- In-container pytest and smoke checks create repeatable verification evidence.
- Logs and JSON artifacts in `outputs/` are the reproducible proof trail.

## Teaching and Extension Notes
1. Keep deterministic contracts explicit before extending feature scope.
2. Add new endpoint tests in `tests/` before changing runtime behavior.
3. Preserve Docker-first verification in CI/local scripts to avoid environment drift.
4. Extend `outputs/example_requests.json` and `example_responses.json` whenever new contracts are added.
5. Keep `outputs/logs/` as evidence snapshots for every meaningful run.
6. When debugging, start with `test_results.log` then `smoke_test.log` to isolate test-vs-runtime issues quickly.

## Reference Artifacts
- Current snapshot document:
  - `pocs/04f/outputs/POC_04f_SUMMARY.md`
- Thread initialization teaching artifact:
  - `pocs/04f/outputs/POC_04f_THREAD_INIT.md`
- Kickoff context artifact:
  - `pocs/04f/outputs/POC_04f_kickoff_prompt.md`

## Snapshot Status
POC 04f currently demonstrates a deterministic Docker-first verification loop with:
- real endpoint tests (no placeholder-only testing)
- passing in-container pytest
- passing smoke tests
- reproducible log/output evidence under `outputs/`
