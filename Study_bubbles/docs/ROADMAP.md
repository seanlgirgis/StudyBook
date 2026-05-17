# ROADMAP

## Iteration 0
Project scaffold and governance/memory docs.

## Iteration 1
Preserve current BOA artifact under `legacy/` and `outputs/baseline/`.

## Iteration 2
Roadmap and contract pivot.

## Iteration 3
Create tiny 3-bubble topic data file.

## Iteration 4
Create topic validator.

## Iteration 5
Create minimal multi-file viewer / builder (historical/deprecated).
Status: historical/deprecated work; not part of active acceptance.

## Iteration 6
Generated Output Rule and Package Path Cleanup.

Purpose:
- Record generated-output rule.
- Historical note only: record local-server testing behavior for deprecated multifile output.
- Review duplicate `build_topic.py` package path issue.
- Do not delete blindly; inspect before cleanup.
Status: historical/deprecated context for multi-file; not part of active acceptance.

## Iteration 7
Create minimal single-file builder that embeds:
- organized metadata
- CSS
- app shell
- topic JSON data
- JavaScript
- build metadata

## Iteration 8
Expand tiny demo to 5 and 7 bubbles.

## Iteration 9
Parent/child topic navigation spike.

## Iteration 10
BOA reference behavior review, not automatic migration.

## Current Acceptance Direction (Post Iteration 11)
- Primary acceptance artifact: `outputs/single_file/*.html`.
- Primary smoke targets:
  - `outputs/single_file/python_overview.html`
  - `outputs/single_file/pandas.html`
- Multi-file output is deprecated historical/debug only, not active acceptance.
- Local HTTP server testing is removed from active acceptance.

## Next Active Step
- Iteration 14 (in progress): grandchild navigation spike.
- Validate/rebuild overview/evidence/new-grandchild plus case-study siblings, then run manual browser smoke for three-level navigation flow.
- Release-gate planning pointer: see `docs/V1_RELEASE_PLAN.md` for the three major gates to v1.0 (`v0.7`, `v0.9`, `v1.0`).
