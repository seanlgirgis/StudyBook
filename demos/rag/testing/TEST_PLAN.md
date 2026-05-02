# Test Plan

## Phase 1: POC Testing

Each POC must include at least one test or smoke check.

## Phase 2: Integrated Testing

The integrated solution must test the full flow:

Website chat widget
→ FastAPI backend
→ RAG retrieval
→ cited answer
→ intake summary
→ escalation decision
→ outcome event
→ dashboard/report

## Phase 3: Deployment Testing

Test after Docker and ECS deployment:

- Health endpoint
- Chat endpoint
- Logs visible
- Expected response returned
- Cleanup works
