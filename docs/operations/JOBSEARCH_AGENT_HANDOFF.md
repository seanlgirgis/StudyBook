# JobSearch Agent Handoff

Purpose: one durable handoff for any agent (or future you) to run JobSearch from StudyBook with consistent outputs, tracking, and multi-machine continuity.

## Canonical Setup

- StudyBook launchpad repo: `D:\StudyBook`
- Managed JobSearch repo: `D:\StudyBook\temp\jobsearch`
- Managed website repo: `D:\StudyBook\temp\seanlgirgis.github.io`

Restore managed repos on a new machine:

```powershell
cd D:\StudyBook
pwsh .\scripts\ops\restore_managed_repos.ps1
```

Launch JobSearch from StudyBook:

```powershell
pwsh .\scripts\ops\open_jobsearch.ps1
```

## What The JobSearch System Does

High-level flow:
1. Intake job posting text.
2. Run triage/applied-before checks.
3. Decide `APPLY`, `HOLD`, or `SKIP`.
4. If `APPLY`, generate tailored resume + cover artifacts.
5. Render final outputs (`.md` + `.docx`).
6. Update metadata status/history.
7. After user confirms submission, mark `APPLIED`.

## Source Of Truth And Key Data

- Career profile source of truth:
  - `D:\StudyBook\temp\jobsearch\data\source_of_truth.json`
- Job folders:
  - `data/jobs/<job_id>/...` (inside JobSearch repo)
- Generated artifacts:
  - `data/jobs/<job_id>/generated/`

## Resume/Cover Build Pipeline

Required system artifacts per job:
- `generated/resume_intermediate.json`
- `generated/cover_intermediate.json`

Rendered outputs per job:
- `generated/resume.md`
- `generated/cover.md`
- `generated/resume.docx`
- `generated/cover.docx`

Render commands:

```powershell
python scripts/05_render_resume.py --uuid <uuid-or-prefix>
python scripts/08_render_cover_letter.py --uuid <uuid-or-prefix>
```

Auto-pipeline wrapper from StudyBook:

```powershell
pwsh .\scripts\ops\run_jobsearch_pipeline.ps1 -IntakeFile "intake\00024.example.md" -Method "LinkedIn"
```

Or resume existing UUID:

```powershell
pwsh .\scripts\ops\run_jobsearch_pipeline.ps1 -Uuid "<uuid>" -Method "LinkedIn"
```

## What Must Be Recorded

Every job should keep accurate `metadata.yaml` tracking, including:
- `uuid`
- `job_id`
- `company`
- `role`
- `location`
- `status` (`NEW|HOLD|READY|APPLIED|REJECTED|INTERVIEW|OFFER|CLOSED`)
- `application.applied` (bool)
- `application.applied_date`
- `application.applied_method`
- `application.history[]` (timestamped status events and notes)

Status expectations:
- After artifact generation/review: `READY`
- After actual submission: `APPLIED` + history entry
- Interview/rejection/closure: append history entry each time

## Daily Operating Contract

Per job:
1. Check applied-before first.
2. Decide apply/hold/skip with clear rationale.
3. If apply, generate tailored artifacts only (no generic resume).
4. Keep claims factual and evidence-based.
5. Update metadata + history.

Daily cadence reference:
- `docs/operations/JOB_SEARCH_DAILY_ENGINE.md`

Detailed direct-mode behavior:
- `docs/operations/jobsearch_direct_mode_playbook.md`

## Relative Path Policy (Critical)

- Use repo-relative paths in scripts and commands.
- Avoid hardcoded machine-specific absolute paths in tracked files.
- Use StudyBook env keys when needed:
  - `STUDYBOOK_JOBSEARCH_ROOT`
  - `STUDYBOOK_WEBSITE_ROOT`

## Multi-Machine Recovery Checklist

On another machine:
1. Clone/pull `D:\StudyBook`.
2. Restore managed repos:
   - `pwsh .\scripts\ops\restore_managed_repos.ps1`
3. Run StudyBook env bootstrap and seed registration if needed.
4. Launch JobSearch via StudyBook wrapper:
   - `pwsh .\scripts\ops\open_jobsearch.ps1`
5. Continue pipeline with same workflow and tracking rules.
