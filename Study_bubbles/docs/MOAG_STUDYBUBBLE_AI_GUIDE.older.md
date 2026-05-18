# MOAG StudyBubble AI Guide

## Purpose
This is the universal operating guide for using StudyBubble with any GenAI system to study topics incrementally.

## Start Here
- I want to study a topic using StudyBubble.
- Do not build the whole map in one shot.
- Work one cluster at a time.
- First teach, then propose bubbles, then update files only when asked.
- Use relative paths from the StudyBook repository root.

## Copy/Paste Kickoff Prompt
```text
I want to study <TOPIC> using StudyBubble.
Use this MOAG.
Mode: teaching first.
Work one cluster at a time.
Do not create the full map yet.
Start by proposing the first 5-10 bubble cluster and the study path.
```

## How To Use This Guide With Any GenAI
1. Paste or upload this guide into the new AI session.
2. Tell the AI your current study topic.
3. Tell the AI your mode: teaching, authoring, Codex implementation, or debug.
4. Tell the AI to work incrementally, not to build the whole map in one shot.

## Path Rules (Relative-First)
- All paths in instructions should be relative to the StudyBook repository root.
- Do not hardcode `D:\Workarea\StudyBook` in generated project instructions.
- Absolute paths are allowed only in the clearly marked Sean local example section.
- StudyBook repository root: `.`
- StudyBubble engine path: `Study_bubbles/`
- Study topic workspace path: `study_maps/`
- Engine demo topic path: `Study_bubbles/topics/`
- Engine demo generated HTML path: `Study_bubbles/outputs/single_file/`
- Engine demo layout path: `Study_bubbles/layouts/`
- Real project container path: `study_maps/<ProjectName>/` with `bubbles.ini`
- Real project topic path: `study_maps/<ProjectName>/topics/`
- Real project generated HTML path: `study_maps/<ProjectName>/outputs/`
- Real project layout path: `study_maps/<ProjectName>/layouts/`

## Sean's Current Local Example
This section is intentionally absolute-path based for local machine context.
- StudyBook root example: `D:\Workarea\StudyBook`

## Environment And Command Rules
From StudyBook root:
```powershell
.\env_setter.ps1
cd Study_bubbles
python -m pytest -q
```

Build engine demo from `Study_bubbles`:
```powershell
python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --out outputs\single_file\<topic_id>.html --mode single-file
```

Build with layout from `Study_bubbles`:
```powershell
python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --layout layouts\<topic_id>.layout.json --out outputs\single_file\<topic_id>.html --mode single-file
```

Real project container build:
```powershell
cd study_maps\<ProjectName>
..\..\scripts\bubbles.ps1 build
```

Layout sync and rebuild from active container:
```powershell
..\..\scripts\bubbles.ps1 sync-layout
```

## Modes Of Work
- Teaching mode:
  Explain one cluster at a time. No file edits.
- Authoring mode:
  Propose bubbles, links, groups, and study paths. No file edits.
- Codex implementation mode:
  Create or update files only when the user asks, then run tests/builds and report results.
- Debug mode:
  Fix StudyBubble engine behavior only when something is broken.

## Incremental Rule (Mandatory)
- Work one cluster per session.
- Keep each cluster to 5 to 10 bubbles max.
- Stop after finishing that cluster and report the next recommended cluster.
- Do not continue expanding without explicit user approval.

## Authoring Standards
- Use required node fields: `id`, `label`, `size`, `group`, `definition`.
- Use recommended fields where useful: `whyItMatters`, `safeSentence`, `commonTrap`, `interviewAnswer`, `relatedQuestions`, `note.summary`, `note.image`, `externalLinks`.
- Keep interview wording safe and factual.
- Do not invent career experience or false production ownership claims.

## Generated Files Are Not Source Of Truth
- Do not hand edit `outputs/single_file/*.html`.
- Edit source files instead:
  - topic JSON in `topics/`
  - viewer files in `viewer/`
  - builder/validator files in `src/study_bubbles/`
- Rebuild generated HTML after source edits.

## Layout Workflow
1. Open generated single-file HTML.
2. Turn on drag mode and adjust layout.
3. Click `Export Layout`.
4. Run `..\..\scripts\bubbles.ps1 sync-layout` from the active container folder.
5. Re-open rebuilt HTML and continue tuning incrementally.

## Minimum Handoff Packet
When moving to another AI session, minimum upload/paste:
- this MOAG
- `STUDYBUBBLE_SESSION_STATE.md` if topic exists
- topic plan if topic exists
- topic JSON if topic exists

## When To Return To StudyBubble Engine Project
Return to engine-level work only for:
- build failure
- viewer bug
- layout sync problem
- broken image handling
- navigation issue
- serious console error
- feature gap that blocks actual studying

## Mental Model
Keep this progressive learning model:
- bubble -> cluster -> island -> city -> continent
