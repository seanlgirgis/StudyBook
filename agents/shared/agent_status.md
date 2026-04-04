# Agent Status

## Current Run (2026-04-04)

**Task ID:** TB-20260404-03  
**Task Type:** ENHANCEMENT  
**Goal:** Implement triage-first gate so job artifacts are generated only after an APPLY decision.

### Changes Implemented

1. Added triage script
- scripts/jobsearch/job_triage.ps1
- Inputs: posting text path + optional company/role/location overrides
- Outputs: data/jobs/_triage/latest_triage.json
- Performs:
  - exact applied-before check against existing metadata
  - lightweight similarity against previously applied raw intake files
  - fit scoring + decision (APPLY|HOLD|SKIP)

2. Added process-if-apply script
- scripts/jobsearch/process_job_if_apply.ps1
- Requires triage file + input text path
- Blocks processing unless triage decision is APPLY (unless -OverrideDecision)
- Creates new job scaffold and metadata from triage context

3. Updated playbook
- docs/operations/jobsearch_direct_mode_playbook.md
- Added explicit Stage 1 (Triage) and Stage 2 (Process If Apply) commands

### Validation

- Command parse/help checks passed:
  - scripts/jobsearch/job_triage.ps1 -?
  - scripts/jobsearch/process_job_if_apply.ps1 -?

### Assumptions

- User wants a repeatable gate that reduces wasted generation cycles on weak/duplicate jobs.

### Risks

- Similarity logic is lightweight keyword Jaccard (not FAISS); edge-case false positives/negatives may still occur and should be reviewed for borderline decisions.

### Next Step

- Use triage-first dialogue for every new posting, then process only APPLY decisions.

---

**Run completed:** 2026-04-04  
**Status:** DONE
