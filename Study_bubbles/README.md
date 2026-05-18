# study_bubbles

## What This Is
study_bubbles is a small, static, data-driven study map system project inside StudyBook.

## Why It Exists
The goal is to transform one topic data file into a reusable interactive study bubble map through a repeatable Python validation/build pipeline.

## Current Boundary (Intentionally Simple)
For now this project stays static, inspectable, and minimal.

- no React
- no npm
- no backend
- no database
- no framework migration
- no cloud deployment work

## Core Pipeline Direction
One topic data file
-> validator/builder
-> standalone single-file HTML

## Engine vs Container
`Study_bubbles/` is the engine. Real study projects should run as independent containers.

Any folder containing `bubbles.ini` is a StudyBubble container. The current working directory is the active container root.

Engine demo flow (legacy/demo-safe):
- `Study_bubbles/topics/`
- `Study_bubbles/layouts/`
- `Study_bubbles/outputs/single_file/`

Real study container flow:
- `study_maps/<ProjectName>/bubbles.ini`
- `study_maps/<ProjectName>/topics/`
- `study_maps/<ProjectName>/layouts/`
- `study_maps/<ProjectName>/outputs/`
- `study_maps/<ProjectName>/assets/`
- optional `study_maps/<ProjectName>/notes/` or `docs/`

Normal container commands (run from `study_maps/<ProjectName>`):
- `../../scripts/bubbles.ps1 build`
- `../../scripts/bubbles.ps1 sync-layout`

## Source vs Output Rule
Maintained source files (engine + active container):
- `viewer/bubble_viewer.html`
- `viewer/bubble_viewer.css`
- `viewer/bubble_viewer.js`
- `topics/*.studybubble.json` (engine demos)
- `<container>/topics/*.studybubble.json` (real study projects)
- `src/study_bubbles/*.py`

Generated output artifacts:
- `outputs/single_file/**`
- `outputs/multifile/**` (deprecated historical/debug artifact, not active acceptance)

Generated HTML files are output, not hand-maintained source.

## Topic File Rule
One topic should normally be represented by one data file.

Examples:
- `topics/tiny_capacity_demo.studybubble.json`
- `topics/python_overview.studybubble.json`
- `topics/pandas.studybubble.json`

## Active Output
- `outputs/single_file/<topic_id>.html`
- one standalone HTML per topic
- topic data embedded in HTML
- CSS/JS embedded in HTML
- opens directly from File Explorer/browser without local HTTP server

Deprecated historical output:
- `outputs/multifile/**` remains for legacy/debug reference only.
- It is not part of active acceptance criteria.

## BOA Role
`BOA_Terminology_Bubble_Map_v3.html` is preserved as a reference prototype for behavior ideas.
It is not the first required migration target.

## First Real Build Target
The first implementation target is `tiny_capacity_demo.studybubble.json` with staged growth:
- 3 bubbles: Telemetry, Baseline, Forecast
- 5 bubbles: + Dashboard, Decision
- 7 bubbles: + Threshold, Owner
