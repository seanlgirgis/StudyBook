# 03h_retrieval_evaluation

## Purpose
Run retrieval test cases and report whether expected source documents appear in top matches.

## What This Tiny POC Teaches
How to measure retrieval quality with repeatable fixtures and metrics.

## Input Files
Query test set, expected source docs, and retrieval pipeline outputs.

## Expected Outputs
Evaluation report with hit@k style checks and failure examples.

## Command (Planned)
`powershell
python -m src.evaluate_retrieval
`

## What Is Intentionally Not Included Yet
No LLM judge, no online telemetry, no production benchmark harness.

## Retrieval Ladder Fit
Stage 8: validates readiness before answer-with-citations milestone.
