# JobSearch + Website Context Note

**Date:** 2026-04-03
**Owner:** Codex
**Purpose:** Durable context for resume source-of-truth and personal website support.

## Confirmed Resume Source of Truth

- Canonical file: `D:\StudyBook\temp\jobsearch\data\source_of_truth.json`
- This file contains the authoritative structured profile for:
  - personal identity metadata,
  - target roles,
  - summary,
  - education/certifications,
  - skills inventory,
  - experience timeline,
  - projects and highlights.

## How I Should Use It

- Treat this JSON as first-priority truth for all job-search support tasks.
- If there is a mismatch between ad hoc notes and this JSON, this JSON wins unless user explicitly overrides.
- Prefer deriving resume bullets, interview stories, and target-role matching from quantified achievements in this file.

## Personal Website Repo Familiarity

Repository: `D:\StudyBook\temp\seanlgirgis.github.io`

### Observed architecture

- Main generator: `generate.py`
- Build model: YAML-driven layouts + shared content store
- Data folder: `data\store.yaml` + target-specific layout YAML files
- Renderer layer: `renderers\docx_renderer.py`, `html_renderer.py`, `pdf_renderer.py`, `md_renderer.py`
- Outputs: `resume.*`, `cv.*`, component HTML, sitemap/robots assets

### Environment notes

- Repo `env_setter.ps1` points to `C:\py_venv\resume_venv`.
- JobSearch project uses `C:\py_venv\JobSearch`.
- StudyBook project uses `C:\py_venv\proj_educate`.
- Keep venv intent explicit per repo to avoid cross-project dependency drift.

## Practical Working Model Going Forward

1. Resume logic and tailoring: anchor to `source_of_truth.json`.
2. Website updates: map desired resume/story updates into YAML content/layout files in website repo.
3. Keep StudyBook as command center; keep JobSearch and website as focused runtime repos with wrappers and documented handoff.

## Immediate Use Cases Enabled

- Targeted role-pack generation (Senior Data Engineer, Cloud Data Architect, AI/Data platform roles).
- Consistent ATS + narrative alignment across JobSearch outputs and personal site artifacts.
- Faster profile refresh cycles when new achievements are added to source-of-truth JSON.
