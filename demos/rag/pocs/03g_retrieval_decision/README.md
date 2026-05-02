# 03g_retrieval_decision

## Purpose
Decide whether to retrieve, clarify, or fallback based on confidence, ambiguity, and top-match quality.

## What This Tiny POC Teaches
How to apply rule-based gating over retrieval outputs for safer behavior.

## Input Files
Hybrid retrieval top results plus configurable thresholds/rules.

## Expected Outputs
Decision object: retrieve|clarify|fallback with reasons and evidence.

## Command (Planned)
`powershell
python -m src.retrieval_decision
`

## What Is Intentionally Not Included Yet
No full chat policy engine and no escalation implementation yet.

## Retrieval Ladder Fit
Stage 7: bridges raw retrieval scores into actionable assistant behavior.
