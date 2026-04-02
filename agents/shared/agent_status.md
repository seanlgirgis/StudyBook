## Task ID
- TB-20260402-13

## Topic
- Improve MongoDB connection proof diagnostics to troubleshoot Atlas TLS handshake failures

## Task Type
- FIX

## Reasoning Depth
- standard

## Risk Level
- low

## Allowed Scope
- bounded

## Files Read
- poc/connection_proofs/python/mongo_connection_proof.py
- user-provided MongoDB error output from shell

## Files Modified
- poc/connection_proofs/python/mongo_connection_proof.py
- agents/shared/task_register.md
- agents/shared/open_loops.md
- agents/shared/agent_status.md

## Plan
1. Add runtime diagnostics that help identify TLS/client mismatches.
2. Add explicit TLS configuration options for Atlas troubleshooting.
3. Keep script read-only behavior unchanged.

## What Was Done
- Added diagnostics output fields:
  - Python version
  - OpenSSL version
  - PyMongo version
  - certifi availability/path
- Added explicit client option building based on URI/Atlas host.
- Added optional flags:
  - `--tls-ca-file`
  - `--insecure-skip-tls-verify` (troubleshooting only)
- Kept proof behavior read-only (`ping` + list DB names).

## Validation
- Runtime execution not performed in this sandbox due Python launcher restriction in this environment.
- Script shape/logic validated by direct file inspection after edit.

## Decisions
- No architecture-level decision; this is a targeted troubleshooting enhancement.

## Assumptions
- Atlas URI and credentials are already present in your local `.env.local`.

## Issues / Risks
- `--insecure-skip-tls-verify` should only be used for temporary debugging, never for steady-state usage.

## Parking Lot Added
- none

## Open Loops Updated
- Added and closed `LOOP-010`.

## Next Step
- Run updated script locally and compare diagnostics output to isolate TLS handshake root cause.
