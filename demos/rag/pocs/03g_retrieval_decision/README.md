# 03g_retrieval_decision

## POC Name
`03g_retrieval_decision`

## Purpose
Build a deterministic retrieval-decision layer on top of `03f_hybrid_retrieval` results.

This POC does not perform retrieval itself. It inspects retrieval evidence and assigns a quality/confidence decision label for downstream handling.

## Why This Exists
`03f` returns ranked candidates and scores, but it does not decide whether those results are strong, ambiguous, weak, or unusable.

`03g` exists to make that decision explicit, testable, and reusable before any answer generation or business response behavior is introduced.

## Retrieval Ladder Position
- `03f_hybrid_retrieval`: produces ranked hybrid candidates
- `03g_retrieval_decision`: decides retrieval confidence/quality class
- future steps: use decision output for clarification UX, fallback behavior, and evaluation

## Expected Input
- hybrid retrieval result payload from `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json` (or compatible structure)
- deterministic decision configuration (thresholds, gap rules, close-candidate rules)

## Expected Output
A structured retrieval-decision object with:
- decision label
- confidence band or score
- reason codes
- key evidence values (top score, score gap, close-candidate count, source diversity)
- recommended downstream route (for later POCs)

## Expected Decision Labels
- `strong_match`
- `ambiguous_match`
- `weak_match`
- `no_match`
- `needs_clarification`

## What 03g Must Not Do
- generate customer answers
- call an LLM
- decide final business response
- ask live clarification questions
- rebuild `03d`, `03e`, or `03f` artifacts
- duplicate prior retrieval logic
- move anything into `integrated/servicecall-ai`

## Deliverables In This Step
Design documentation only:
- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`

No implementation files are introduced in this design step.
