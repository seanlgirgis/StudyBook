# JobSearch Direct-Mode Playbook (StudyBook)

Last updated: 2026-04-04

## Goal
Run job search directly from this repository with Codex as the primary runner. Resume and cover generation is manual, role-fit, and evidence-based.

## Source Of Truth
- Data root: `data/`
- Jobs: `data/jobs/<job_id>/`
- Master profile: `data/source_of_truth.json` and `data/master/*`
- Generated artifacts: `data/jobs/<job_id>/generated/*`

## Operating Rules (Always)
1. Never submit a generic resume.
2. Always run applied-before checks before creating new artifacts.
3. Track every status change in `metadata.yaml`.
4. Keep one final submitted pair per job: `generated/resume.docx` and `generated/cover.docx`.
5. Use relative paths only.
6. Intermediate files are required for resume and cover generation; renderer scripts convert them to markdown previews and final docx deliverables.

## Direct-Mode Contract
Codex acts as the pipeline:
1. Ingest job text.
2. Decide apply or skip with explicit rationale.
3. If apply: create job folder (`<sequence>_<uuid8>`), intake/raw/metadata.
4. Create tailored artifacts directly in `generated/`.
5. Set status transitions (`NEW -> READY -> APPLIED`) with history updates.

## Standard Workflow
1. Store new job text in `intake/` (or provide it in chat).
2. Run applied-before checks:
   - exact company + role check in prior metadata
   - lightweight similarity against recent `raw/raw_intake.md`
3. Make apply decision:
   - `APPLY`: continue
   - `HOLD`: stop and record reason
   - `SKIP`: stop and record reason
4. Generate and review resume/cover.
5. Mark `READY`.
6. After submission, mark `APPLIED` with date/method/notes.

## Optional Helper Script
Use only to scaffold a new job folder quickly:

```powershell
./scripts/process_job_direct.ps1 -Intake intake/intake.md -Company "Loopback Health" -Role "Data Engineer" -Location "Dallas, TX"
```

This script does not call any external model or Python pipeline. It only creates structure and metadata.

## Required Tracking Fields In `metadata.yaml`
- `uuid`
- `job_id`
- `company`
- `role`
- `location`
- `status` (`NEW|HOLD|READY|APPLIED|REJECTED|INTERVIEW|OFFER|CLOSED`)
- `application.applied` (true/false)
- `application.applied_date` (YYYY-MM-DD or null)
- `application.applied_method` (LinkedIn, Company Website, Referral, etc.)
- `application.history[]` with timestamped updates

## Status Update Policy
- After generation review: set `status: READY`
- After submission: set `status: APPLIED` and append history
- Interview/reject/no-response updates always append history

## Weekly Maintenance
1. Review all jobs in `HOLD` or `READY`.
2. Follow up on `APPLIED` jobs older than 7 days.
3. Archive final outcomes (`REJECTED`, `CLOSED`) with a closing note.
4. Refresh master profile when new shipped outcomes become resume-relevant.

## Assistant Commitments (Codex)
For each requested job, I will:
1. Run applied-before checks first.
2. Decide apply/hold/skip with clear reasons.
3. Produce role-fit artifacts (no inflated claims).
4. Flag weak wording before submission.
5. Keep metadata accurate and current.

## Artifact Policy
- Required pipeline: `resume_intermediate.json` + `cover_intermediate.json` -> renderer scripts -> `resume.md`, `cover.md`, `resume.docx`, `cover.docx`.
- Required outputs per job: `generated/resume.md`, `generated/cover.md`, `generated/resume.docx`, `generated/cover.docx`.
- Intermediates remain in `generated/` as system artifacts for rerendering and audit.
- Use relative paths only.

## Rendering Commands
```powershell
python scripts/05_render_resume.py --uuid <uuid-or-prefix>
python scripts/08_render_cover_letter.py --uuid <uuid-or-prefix>
```


## Stage 1 (Triage)
Run triage first (no artifact generation yet):

```powershell
./scripts/jobsearch/job_triage.ps1
```

Review `data/jobs/_triage/latest_triage.json` and proceed only when decision is `APPLY`.

## Stage 2 (Process If Apply)
Create a new job folder only after triage passes:

```powershell
./scripts/jobsearch/process_job_if_apply.ps1 -TriagePath data/jobs/_triage/latest_triage.json
```

Then generate intermediates and render outputs (`resume.md`, `cover.md`, `resume.docx`, `cover.docx`).
