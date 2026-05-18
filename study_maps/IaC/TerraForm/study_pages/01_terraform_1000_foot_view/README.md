# Terraform 1000-Foot View

## Purpose
Teach the first Terraform mental model before deeper workflow and state details.

## What This Tutorial Teaches
- Terraform and IaC framing
- desired state
- providers/resources
- plan/apply flow
- state and drift
- team safety controls

## Suggested Study Path
Terraform -> IaC -> Desired State -> Providers/Resources -> Plan -> Apply -> State -> Drift -> Team Safety

## Key Ideas
- Terraform is desired-state infrastructure management, not script execution only
- plan is the safety checkpoint
- state links code to managed reality
- drift and team controls matter for teams

## Safe Interview Answer
Terraform defines desired infrastructure in code, compares intent with managed reality, previews change in plan, and applies approved changes with state-aware controls.

## Common Traps
- treating Terraform as just scripts
- skipping plan review
- ignoring state sensitivity
- assuming manual changes cannot impact Terraform

## Continue To
- Core Workflow map
- State/Drift/Backends map
- Providers/Resources map

## No Lab Required
This orientation tutorial is conceptual and map-first; no runnable lab required.
