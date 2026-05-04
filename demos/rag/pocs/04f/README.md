# POC 04f - Deployable Service Layer Integration

## Purpose
POC 04f integrates the deterministic FastAPI RAG service from `pocs/04e` into a container-ready service layer for Docker/ECS/Fargate style deployment, while preserving all deterministic and validation behavior.

## Scope For This Kickoff
- Create the POC 04f structure.
- Persist the approved kickoff prompt and constraints.
- Prepare design docs before implementation.

## Non-Goals
- No threshold tuning.
- No LLM calls.
- No customer data.
- No architecture jump into `integrated/servicecall-ai`.
