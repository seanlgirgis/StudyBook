# Design

## Purpose
Provide a beginner-first launchpad for Databricks + PySpark learning with local validation before any cloud dependency.

## Design Rules
- Documents and contracts are defined before lesson code.
- Every check prints clear pass/missing/fail signals.
- Local PySpark (`local[*]`) is the only runtime requirement for gate 1.

## Phase 1 Components
- `docs/`: design intent, constraints, test plan, environment notes
- `scripts/`: local environment check utilities
- `src/`: smoke-test runnable script
- `tests/`: minimal verification tests
- `outputs/validation/`: captured proof artifacts

## Non-Goals
- Databricks workspace config
- AWS resources
- Paid cloud compute
