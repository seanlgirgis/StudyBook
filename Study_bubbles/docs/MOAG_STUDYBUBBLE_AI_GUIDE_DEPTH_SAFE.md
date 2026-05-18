# MOAG StudyBubble AI Guide

## Purpose

This is the universal operating guide for using StudyBubble with any GenAI
system to study topics incrementally.

This guide is for **learning-topic projects**, not normal engine development.
Use it when studying a topic such as Terraform, Power BI, AWS, Kubernetes,
OpenTelemetry, SQL, Python, Tableau, or another StudyBook subject.

StudyBubble should be treated as a learning tool unless something breaks.

---

## Core Operating Rule

```text
Teach first.
Propose bubbles second.
Update files only when asked.
Build/test only to validate the learning material.
Return to engine development only when StudyBubble actually breaks.
```

Do not turn every learning-topic discussion into StudyBubble engine work.

---

## Start Here

Use this starting posture:

```text
I want to study a topic using StudyBubble.
Do not build the whole map in one shot.
Work one cluster at a time.
First teach, then propose bubbles, then update files only when asked.
Use the active StudyBubble container as the project root.
```

---

## Copy/Paste Kickoff Prompt

```text
I want to study <TOPIC> using StudyBubble.

Use this MOAG.

Mode: teaching first.

Work one cluster at a time.

Do not create the full map yet.

Start by teaching the topic at a simple 1000-foot level.

Then propose the first 5-10 bubble cluster and one study path.

Do not update files until I explicitly say to implement.
```

---

## Correct Communication Model

For learning-topic projects, communicate like this:

```text
1. Teach the concept simply.
2. Explain why it matters.
3. Propose a small bubble cluster.
4. Propose links/study paths.
5. Wait for approval before file changes.
6. Build/test only after implementation is requested.
```

Avoid this unless debugging is explicitly requested:

```text
- broad engine refactoring
- speculative StudyBubble features
- new script architecture
- moving artifacts around without cause
- full-course generation in one shot
```

---

## Current Accepted Architecture

```text
Study_bubbles/
= central StudyBubble engine

scripts/bubbles.ps1
= central StudyBook user command

study_maps/**/<ContainerName>/
= independent StudyBubble learning container
= identified by the presence of bubbles.ini
```

A learning container owns its own:

```text
bubbles.ini
topics/
layouts/
outputs/
assets/
README.md
STUDYBUBBLE_SESSION_STATE.md
topic notes/materials
```

A learning container must **not** need its own copied `scripts/` folder.

Do not copy per-project build scripts into every study topic. That creates a
script zoo.

---

## Container Root Rule

The container root is not determined by folder depth.

The container root is:

```text
the folder containing bubbles.ini
```

Examples of valid containers:

```text
study_maps/TerraForm/
study_maps/IaC/TerraForm/
study_maps/Data/PowerBI/
study_maps/Cloud/AWS/
study_maps/Observability/OpenTelemetry/
```

Moving a container deeper under `study_maps/` should **not** require changing
local project paths such as:

```text
topics_dir = topics
layouts_dir = layouts
outputs_dir = outputs
assets_dir = assets
```

Those paths are resolved from the folder containing `bubbles.ini`.

---

## Command Rule: Stable Command, No Dot-Counting

Do **not** teach users to count folder levels with commands such as:

```powershell
..\..\scripts\bubbles.ps1 build
..\..\..\scripts\bubbles.ps1 build
```

That is a fallback/debug pattern only, not the product workflow.

The normal command should be stable from any StudyBubble container:

```powershell
bubbles build
bubbles sync-layout
```

If PowerShell requires the script name:

```powershell
bubbles.ps1 build
bubbles.ps1 sync-layout
```

Expected setup:

```text
StudyBook/scripts is available on PATH through env_setter.ps1,
PowerShell profile setup, or equivalent StudyBook shell initialization.
```

The central command must preserve the current working directory as the active
container so it can read:

```text
./bubbles.ini
```

from the folder where the user is standing.

---

## Path Rules

Use paths relative to the active StudyBubble container whenever possible.

```text
StudyBook repository root:
.

StudyBubble engine path:
Study_bubbles/

Central StudyBook scripts path:
scripts/

Study topic workspace path:
study_maps/

Real project container path:
study_maps/**/<ContainerName>/

Real project config:
<container>/bubbles.ini

Real project topic path:
<container>/topics/

Real project layout path:
<container>/layouts/

Real project generated HTML path:
<container>/outputs/

Real project assets path:
<container>/assets/
```

Engine demo paths are allowed only for engine demos/regression tests:

```text
Study_bubbles/topics/
Study_bubbles/layouts/
Study_bubbles/outputs/single_file/
```

Do not use engine demo paths as the normal location for real study projects.

---

## Sean's Local Example

This section is intentionally absolute-path based for Sean's local machine.

```text
StudyBook root:
D:\Workarea\StudyBook

StudyBubble engine:
D:\Workarea\StudyBook\Study_bubbles

Central user command:
D:\Workarea\StudyBook\scripts\bubbles.ps1

Example Terraform learning container:
D:\Workarea\StudyBook\study_maps\IaC\TerraForm

Typical browser Downloads folder:
D:\Users\shareuser\Downloads
```

After StudyBook shell initialization, the command should be stable from the
container folder:

```powershell
cd D:\Workarea\StudyBook\study_maps\IaC\TerraForm
bubbles build
bubbles sync-layout
```

---

## Required `bubbles.ini`

Every real StudyBubble learning container must have a local `bubbles.ini`.

Example:

```ini
[studybubble]
name = LearnTerraform
mode = single-file
default_topic = terraform_1000_foot_view

topics_dir = topics
layouts_dir = layouts
outputs_dir = outputs
assets_dir = assets
downloads_dir = D:/Users/shareuser/Downloads

[projects]
# Optional future map-of-maps references.
# aws = ../../Cloud/AWS
# powerbi = ../../Data/PowerBI
# opentelemetry = ../../Observability/OpenTelemetry
```

Rules:

```text
- The folder containing bubbles.ini is the active StudyBubble container.
- Relative paths in bubbles.ini are resolved from that container folder.
- Absolute paths are used as-is.
- downloads_dir may be absolute or relative.
- default_topic must match a real topic file under topics/.
- If bubbles.ini is missing, the runner should fail fast.
```

### Engine Path Rule

A real learning container should not normally need to define the engine path.

The central command knows where the StudyBook root and StudyBubble engine are
because the wrapper lives under:

```text
StudyBook/scripts/bubbles.ps1
```

So the wrapper can infer:

```text
StudyBook root = parent of scripts/
StudyBubble engine = StudyBook root / Study_bubbles
```

If an `[engine] path = ...` section exists, treat it as optional/debug-only,
not as a required part of normal containers.

---

## Standard Commands

Initialize the StudyBook shell/environment when needed:

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
```

The environment should make the central StudyBook scripts available so the user
can run this from any StudyBubble container:

```powershell
bubbles build
bubbles sync-layout
```

Run engine tests from the engine folder:

```powershell
cd D:\Workarea\StudyBook\Study_bubbles
python -m pytest -q
```

Build a real project container from the container folder:

```powershell
cd D:\Workarea\StudyBook\study_maps\IaC\TerraForm
bubbles build
```

Sync exported layout and rebuild from the container folder:

```powershell
cd D:\Workarea\StudyBook\study_maps\IaC\TerraForm
bubbles sync-layout
```

Direct Python fallback only if needed:

```powershell
python <StudyBookRoot>\Study_bubbles\tools\studybubble.py build
python <StudyBookRoot>\Study_bubbles\tools\studybubble.py sync-layout
```

Relative `..\..\scripts\bubbles.ps1` examples are allowed only as fallback
when PATH/profile setup is not available. They must not be presented as the
normal product workflow.

---

## Engine Demo Commands

Use these only inside the StudyBubble engine project for demos/regression work:

```powershell
cd Study_bubbles

python -m src.study_bubbles.build_topic `
  --topic topics\<topic_id>.studybubble.json `
  --out outputs\single_file\<topic_id>.html `
  --mode single-file
```

Build an engine demo with layout:

```powershell
python -m src.study_bubbles.build_topic `
  --topic topics\<topic_id>.studybubble.json `
  --layout layouts\<topic_id>.layout.json `
  --out outputs\single_file\<topic_id>.html `
  --mode single-file
```

Do not use these as the primary workflow for real learning containers.

---

## Modes of Work

### Teaching Mode

Use when the user is learning.

```text
Explain one cluster at a time.
Use plain language.
Use practical examples.
No file edits.
No full-course generation.
```

### Authoring Mode

Use when designing a StudyBubble map.

```text
Propose bubbles, groups, links, and study paths.
Keep the cluster small.
No file edits unless asked.
```

### Codex Implementation Mode

Use when the user explicitly asks to update files.

```text
Create or update files.
Run build/tests when relevant.
Report files changed and commands run.
Do not hand-edit generated HTML.
```

### Debug Mode

Use only when something breaks.

```text
Fix build failure, viewer bug, layout sync problem, broken image handling,
navigation issue, serious console error, or workflow blocker.
```

---

## Incremental Rule

Mandatory:

```text
Work one cluster per session.
Keep each cluster to 5-10 bubbles max.
Stop after finishing that cluster.
Report the next recommended cluster.
Do not continue expanding without explicit approval.
```

StudyBubble growth model:

```text
bubble -> cluster -> island -> city -> continent
```

---

## Authoring Standards

Required node fields:

```text
id
label
size
group
definition
```

Recommended node fields:

```text
whyItMatters
safeSentence
commonTrap
interviewAnswer
relatedQuestions
note.summary
note.image
externalLinks
childTopics
```

Standards:

```text
- Keep definitions short and useful.
- Use interview-safe language where relevant.
- Do not invent career experience.
- Do not overclaim production ownership.
- Use group colors clearly.
- Keep study paths short and teachable.
```

---

## Group Color Rules

Different subtopics should use different colors.

Topic/group filter buttons should match their bubble colors.

System/action buttons should remain neutral.

Topic/group controls:

```text
Terraform Basics
Terraform Workflow
State
Providers
Resources
Modules
Power BI Modeling
DAX
Publishing
Refresh
```

System/action controls:

```text
Drag Mode
Focus
Fit
Reset View
Export Layout
Reset
Copy buttons
```

Rule:

```text
Topic buttons = study group colors.
System buttons = neutral control styling.
```

---

## Generated Files Are Not Source of Truth

Do not hand-edit generated HTML.

Generated files:

```text
<container>/outputs/*.html
Study_bubbles/outputs/single_file/*.html
```

Edit source files instead:

```text
<container>/topics/*.studybubble.json
<container>/layouts/*.layout.json
<container>/bubbles.ini
Study_bubbles/viewer/
Study_bubbles/src/study_bubbles/
Study_bubbles/tools/
```

Then rebuild.

---

## Layout Workflow

The layout loop is part of acceptance, not optional polish.

Steps:

```text
1. Build the HTML.
2. Open generated HTML directly in the browser.
3. Turn on Drag Mode.
4. Move bubbles.
5. Click Export Layout.
6. Confirm the layout file lands in downloads_dir.
7. Run sync-layout from the active container.
8. Confirm the layout file appears under the container layouts/ folder.
9. Rebuild.
10. Reopen HTML.
11. Confirm positions persisted.
```

Command example from any active container after shell setup:

```powershell
bubbles sync-layout
bubbles build
```

Expected Terraform paths when the active container is
`study_maps/IaC/TerraForm`:

```text
Export staging:
D:/Users/shareuser/Downloads

Persisted layout:
study_maps/IaC/TerraForm/layouts/<topic_id>.layout.json

Generated HTML:
study_maps/IaC/TerraForm/outputs/<topic_id>.html
```

---

## Container Acceptance Checklist

A real StudyBubble container passes only when:

```text
- bubbles.ini exists in the active container root.
- default_topic matches an actual file under topics/.
- topic JSON exists under the container topics/ folder.
- generated HTML is written under the container outputs/ folder.
- layout JSON is written under the container layouts/ folder.
- no real-project artifacts are written into Study_bubbles/topics/.
- no real-project outputs are written into Study_bubbles/outputs/single_file/.
- no per-project scripts folder is needed.
- the same command works regardless of container depth.
- map opens directly in browser.
- map is not a flat row by default.
- group colors are visible on bubbles.
- group filter buttons match bubble colors.
- system buttons are neutral.
- drag/export/sync-layout/rebuild preserves positions.
```

---

## When To Return To StudyBubble Engine Project

Return to StudyBubble engine work only for:

```text
build failure
viewer bug
layout sync problem
broken image handling
navigation issue
serious console error
feature gap that blocks actual studying
wrong output location
wrong layout location
group colors not rendering
layout persistence failure
stable command failure from nested containers
```

Do not return to engine work just because a topic needs better content.

---

## Learning Topic Prompt Template

Use this in a learning project such as LearnTerraform, LearnPowerBI, LearnAWS,
or another topic project.

```text
We are in a StudyBubble learning-topic project.

This is not StudyBubble engine development unless something breaks.

Topic:
<TOPIC>

Mode:
Teaching first.

Use this workflow:
1. Teach the next concept simply.
2. Explain why it matters.
3. Propose a 5-10 bubble cluster.
4. Propose one study path.
5. Wait for approval before updating files.

Do not build the full map.
Do not expand into a full course.
Do not hand-edit generated HTML.
Do not write real-topic artifacts into Study_bubbles/topics or
Study_bubbles/outputs/single_file.

Container path:
study_maps/**/<ContainerName>

Build command from the container:
bubbles build

Layout sync command from the container:
bubbles sync-layout
```

---

## Brand-New Topic Container Test Prompt

Use this to prove StudyBubble works outside the current topic.

```text
We are starting a brand-new StudyBubble learning topic.

Topic:
<TOPIC>

Project container:
study_maps/**/<ContainerName>

Purpose:
This is both a real learning topic and a StudyBubble container feasibility test.

Do not modify the StudyBubble engine unless something breaks.

Create or verify:
- bubbles.ini
- topics/
- layouts/
- outputs/
- assets/
- README.md
- STUDYBUBBLE_SESSION_STATE.md

Do not create a project-local scripts/ folder.

Use central commands from the container:

bubbles build

bubbles sync-layout

Create only a first 5-10 bubble overview cluster.

Before writing files:
1. Teach the 1000-foot concept.
2. Propose groups, bubbles, links, and one study path.
3. Wait for approval.

After implementation:
1. Build.
2. Open generated HTML.
3. Confirm the map renders.
4. Confirm it is not a flat row.
5. Confirm group colors are distinct.
6. Confirm group buttons match bubble colors.
7. Drag 2-3 bubbles.
8. Export layout.
9. Run sync-layout.
10. Rebuild.
11. Confirm positions persist.

Deliver:
- what was created
- files changed
- commands run
- final HTML path
- final layout path
- whether the container workflow passed
- whether anything needs to return to StudyBubble engine project
```

---

## Minimum Handoff Packet

When moving to another AI session, provide:

```text
- this MOAG
- STUDYBUBBLE_SESSION_STATE.md if topic exists
- topic plan if topic exists
- current topic JSON if topic exists
- current layout JSON if layout exists
- notes about any known build/sync issues
```

---

## Final Law

```text
StudyBubble is the engine.
scripts/bubbles.ps1 is the central StudyBook command.
The folder containing bubbles.ini is the active learning container.
Real learning containers own their topics, layouts, outputs, and assets.
Containers may be nested; command syntax should not change with depth.
Learning sessions teach first and implement only when asked.
Engine work happens only when the tool breaks.
```
