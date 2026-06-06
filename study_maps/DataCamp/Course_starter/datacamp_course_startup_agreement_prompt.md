# DataCamp Course Startup Agreement Prompt

Use this prompt at the start of every new DataCamp course chat.

---

We are starting a new DataCamp course inside StudyBook.

## Course identity

Course name:

```text
<PASTE_COURSE_NAME_HERE>
```

Canonical course slug:

```text
<PASTE_STABLE_COURSE_SLUG_HERE>
```

Track context:

```text
<PASTE_TRACK_OR_TRACKS_HERE>
```

Important rule:

The canonical course folder must NOT use a track-relative course number.
The same course may appear in different positions in different tracks.
Track pages own ordering. Course folders use stable slugs.

---

## Repository context

Repository root:

```text
D:\Workarea\StudyBook
```

Canonical DataCamp study root:

```text
D:\Workarea\StudyBook\study_maps\DataCamp
```

Canonical course folder pattern:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\<course_slug>
```

Preferred temporary source handoff folder:

```text
D:\Users\shareuser\Downloads
```

Use relative paths in documentation whenever possible.

---

## Current DataCamp architecture decision

For DataCamp course work, Sean currently wants the active course package
together in one canonical course folder.

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\<course_slug>
```

This folder should contain the active course package:

```text
index.html
README.md
STUDYBUBBLE_SESSION_STATE.md

docs\
  BILL_OF_MATERIALS.md
  COURSE_SETUP_AUDIT.md

source_material\
  README.md
  course_curriculum_outline.md
  transcript_raw_combined.md
  exercise_notes.md
  archive\

study_pages\
  field_guide.md
  field_guide.html
  chapter_01_<chapter_slug>_field_guide.html
  chapter_02_<chapter_slug>_field_guide.html
  ...
  <course_domain>_quick_lookup.html

lab\
  README.md
  00_how_to_run.md
  lab_run_book.md
  sql\
  expected_outputs\
  notes\
  source_archive\
```

Meaning:

```text
study guide + HTML cheat sheet + BOM + transcripts + lab run book + SQL files
= all active course assets under the one canonical course folder
```

Do not separate the active lab package into a distant tutorial folder unless
Sean explicitly asks.

A legacy or secondary tutorial copy may exist, but the active course package
should point to the canonical course folder.

---

## Clarification rule

If Sean gives an instruction that could change folder layout, architecture,
naming, or workflow, ask a short clarifying question before writing a Codex
prompt.

Do not assume.

Example:

```text
When you say “everything together,” do you mean:

A) Everything active inside study_maps\DataCamp\courses\<course_slug>\
including lab SQL files?

or

B) Study material in study_maps and runnable lab material in tutorials,
but linked clearly?
```

Wait for Sean's answer before generating the implementation prompt.

---

## Fast course workflow agreement

For each DataCamp course, avoid many tiny setup iterations.

Use this faster layered order:

```text
1. Capture curriculum + transcript/source files.
2. Create Bill of Materials.
3. Create the accumulated Field Guide Markdown skeleton.
4. Create the accumulated Field Guide HTML overview using the standard dark style.
5. Create one lightweight HTML chapter-guide shell per course chapter.
6. Create one domain-specific Quick Lookup HTML skeleton.
7. Create the course-local Lab Run Book / Lab Guide skeleton under lab\.
8. Capture or create course-local SQL/lab files under lab\sql\ when needed.
9. Start the live DataCamp course pass.
10. Populate each chapter guide during or immediately after that chapter.
11. Patch the Quick Lookup and Lab Guide during the live pass.
12. Add only distilled, cross-chapter knowledge to the accumulated Field Guide.
13. Reconcile all artifacts at course closeout.
```

The setup goal is speed, not perfection.

Create chapter-guide and Quick Lookup shells early, but do not fully author every
chapter before studying it.

Do not spend many rounds polishing setup artifacts before learning.

Only split work into multiple Codex prompts if there is a real blocking reason.

---

## Phase 1 — Capture source material

Sean may provide some or all of these:

```text
1. Course curriculum / outline image
2. Course outline text
3. Video scripts or transcripts
4. Exercise prompts, screenshots, or notes
5. Existing ZIP files containing SQL/lab materials
```

Raw source material belongs under:

```text
study_maps\DataCamp\courses\<course_slug>\source_material\
```

Raw source material is evidence. Do not treat it as final study material.

When a source file is provided through Downloads, Codex should:

```text
1. Read the source file from D:\Users\shareuser\Downloads.
2. Copy the useful content into the canonical course folder.
3. Archive the consumed source file under source_material\archive\ or
   lab\source_archive\, depending on what kind of file it is.
4. Confirm the Downloads copy no longer exists.
5. If moving fails, do not delete the file; report the issue.
```

Use:

```text
source_material\archive\
```

for curriculum/transcript/source evidence.

Use:

```text
lab\source_archive\
```

for lab ZIPs, runnable SQL source packages, or lab input bundles.

---

## Phase 2 — Build Artifact 1: Bill of Materials

Create the Bill of Materials before writing or expanding the Field Guide.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\docs\BILL_OF_MATERIALS.md
```

The Bill of Materials should include:

```text
- course title
- canonical slug
- track context
- source inventory
- curriculum image status
- transcript status
- exercise notes status
- lab source status
- chapter list
- lesson/video list
- topic list
- function/command/operator list
- data type list
- SQL/Python/etc. pattern list as applicable
- accumulated field guide targets
- chapter guide targets
- quick lookup targets
- lab run book / lab guide targets
- fast-review topics
- slow-down topics
- interview-important topics
- open questions / missing material
```

This is the inventory. It should be concise but useful.

---

## Phase 3 — Build Artifact 2: Field Guide Markdown

Create the Field Guide Markdown under the course study folder.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\field_guide.md
```

The accumulated Field Guide is the whole-course memory map and navigation hub.

It should include:

```text
- all major course ideas
- concise plain-English explanations
- core syntax patterns
- selected generic code samples
- strongest DataCamp-style exercise patterns
- cross-chapter mistakes and corrections
- interview questions and answers
- job/interview translation
- quick memory nuggets
- common traps and edge cases
- links to each detailed chapter guide
- links to the Quick Lookup and Lab Guide
```

Do not turn the accumulated Field Guide into the deepest source for every topic.
Detailed use cases, many examples, chapter-specific mistakes, and chapter-specific
Q&A belong in the chapter guides.

The Field Guide belongs inside the canonical course folder.

---

## Phase 4 — Build Artifact 3: Field Guide HTML Cheat Sheet

Create an HTML cheat sheet from the Field Guide.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\field_guide.html
```

This is the browser cheat sheet Sean will keep open while doing DataCamp and labs.

Style rule:

The HTML Field Guide should use the same visual style as the established dark
SQL Windowing Field Guide.

Reference style file:

```text
study_maps\DataCamp\courses\05_postgresql_summary_stats_and_window_functions\study_pages\sql_windowing_field_guide.html
```

Use the same general style system:

```text
- dark GitHub-like background
- IBM Plex Sans / IBM Plex Mono font imports
- CSS variables in :root
- header with badge
- gradient line at top of header
- centered .container layout
- table-of-contents box
- toc-header with three colored dots
- toc-grid / toc-section style
- .section blocks with section-header
- .section-num badges
- dark code blocks
- inline code styling
- .callout boxes
- .nugget boxes
- .diagram blocks
- .vtable table styling
- .compare-grid / .compare-card where useful
- .cheat-grid / .cheat-cell for quick reference sections
- .interview-box for interview translation sections
- back-to-top links
- footer
```

Do not copy content from the Windowing Field Guide into the new course.
Only copy/reuse the style and layout pattern.

Each course must have its own title, badge, table of contents, and sections.

---

## Phase 5 — Build Artifact 4: Chapter Field Guide Shells

Create one detailed HTML chapter guide shell per course chapter.

Preferred naming pattern:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\chapter_01_<chapter_slug>_field_guide.html
study_maps\DataCamp\courses\<course_slug>\study_pages\chapter_02_<chapter_slug>_field_guide.html
...
```

Chapter guides are the deep, searchable teaching books for one chapter.

Each shell should establish:

```text
- chapter title and subtitle
- stable section IDs
- grouped table of contents
- visible search box
- sticky quick navigation
- floating navigation when useful
- problem-based lookup
- detailed use cases
- worked examples
- common mistakes
- interview Q&A
- memory review
- links back to the accumulated Field Guide, Quick Lookup, and Lab Guide
- maximum two-column desktop card layout
- one-column mobile fallback
```

During setup, create lightweight shells only.

Populate each chapter guide during or immediately after studying that chapter.
Do not fully write all chapter guides before the live course pass.

---

## Phase 6 — Build Artifact 5: Domain Quick Lookup

Create one compact, searchable Quick Lookup page.

Preferred naming pattern:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\<course_domain>_quick_lookup.html
```

Examples:

```text
sql_function_quick_lookup.html
python_quick_lookup.html
pyspark_quick_lookup.html
power_bi_quick_lookup.html
linux_command_quick_lookup.html
```

The Quick Lookup should answer:

```text
- What function, command, operator, or pattern do I need?
- What is the smallest useful syntax example?
- What direction rule matters: higher, lower, true/false, ascending/descending?
- What is the most common trap?
```

Keep it compact and searchable.

Do not turn the Quick Lookup into another large Field Guide.

---

## Phase 7 — Build Artifact 6: Course-local Lab Run Book / Lab Guide

Create a Lab Run Book inside the canonical course folder.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\lab\lab_run_book.md
```

The Lab Run Book is the hands-on practice plan.

As the live course progresses, it may mature into a Lab Guide that records
practiced evidence.

It should include:

```text
- lab purpose
- sample dataset design
- table schemas or input data design
- seed data ideas
- chapter-by-chapter lab ideas
- exercises
- expected outputs
- practice checkpoints
- troubleshooting notes
- practiced queries or code
- observed outputs
- mistakes and corrections
- environment/schema/extension evidence when relevant
- future runnable file plan
```

For the first pass, create a skeleton only.
Do not create extra SQL files, Docker files, datasets, or expected outputs unless
Sean explicitly asks.

---

## Phase 8 — Course-local SQL and lab files

When runnable SQL files or lab files are needed, place the active versions under:

```text
study_maps\DataCamp\courses\<course_slug>\lab\
```

Recommended structure:

```text
lab\
  README.md
  00_how_to_run.md
  lab_run_book.md
  sql\
    00_create_schema.sql
    01_create_tables.sql
    02_insert_sample_data.sql
    03_<chapter_or_topic>.sql
  expected_outputs\
    README.md
  notes\
    troubleshooting.md
  source_archive\
```

If there is an older tutorial copy, do not delete it unless Sean explicitly asks.
Mark it as a secondary copy and point back to the canonical course folder.

---

## Phase 9 — Live DataCamp pass

After the Bill of Materials, Field Guide, HTML cheat sheet, Lab Run Book
skeleton, and any needed setup SQL exist, go through the DataCamp course live.

During the live course pass, capture:

```text
- missing examples
- DataCamp-specific wording
- exercise mistakes
- tricky syntax
- shortcuts
- confusion points
- useful additions to the active chapter guide
- compact additions to the Quick Lookup
- evidence additions to the Lab Guide
- only distilled cross-chapter additions to the accumulated Field Guide
- useful SQL/Python/etc. snippets for lab files
```

Recommended cadence:

```text
- every 5–10 meaningful learning interactions: make a small documentation update
- at chapter completion: close the active chapter guide
- at course completion: reconcile all artifacts against the curriculum and exercises
```

The live DataCamp pass is the validation and gap-filling pass.

Do not wait until the end of the course to build every detailed chapter page.

---

## Phase 10 — Course closeout and reconciliation

A DataCamp platform pass does not automatically mean mastery.

At course completion, perform a scoped reconciliation:

```text
1. Compare the curriculum and transcripts to the Bill of Materials.
2. Confirm each chapter guide covers the actual lessons and exercises.
3. Confirm the Quick Lookup contains the important syntax and direction rules.
4. Confirm the Lab Guide records practiced work, observed outputs, and mistakes.
5. Remove placeholders and stale scaffolding.
6. Add missing exact examples from videos or exercises.
7. Confirm the accumulated Field Guide links to all chapter guides.
8. Confirm the course index links to the main guide, chapter guides, Quick Lookup, and Lab Guide.
9. Record the platform completion status.
10. Record the StudyBook mastery status honestly.
```

Recommended status model:

```text
Platform status: PASSED / IN PROGRESS

Documentation coverage: COMPLETE / PARTIAL

Lab coverage: STRONG / DEVELOPING / LIGHT

Recall confidence: STRONG / DEVELOPING / NEEDS REVIEW

Interview readiness: READY / NEEDS REPETITION / NOT YET
```

After a platform pass, the course moves into maintenance and review mode rather
than being treated as permanently mastered.

---

## Teaching style

Teach Sean in small bites.

When Sean pastes an answer or SQL/code:

```text
1. Comment on Sean's solution first.
2. Tell him what is right.
3. Point out the exact issue if something is wrong.
4. Give a small hint before dumping the answer.
5. Give corrected SQL/code only when needed.
6. Capture reusable patterns and mistakes.
```

Every 5–10 meaningful learning interactions, recommend a small StudyBook/Codex
documentation update.

---

## Architecture rules

Current DataCamp course architecture:

```text
study_maps\DataCamp\courses\<course_slug>
= active course package:
  BOM, accumulated Field Guide, chapter Field Guides, Quick Lookup,
  notes, transcripts, session state, Lab Run Book / Lab Guide,
  SQL or code files, expected output notes, troubleshooting notes,
  and source archives.

Study_bubbles
= engine only.

scripts
= shared commands only.
```

Legacy rule note:

The older MOAG separation of study_maps vs tutorials still matters for many
projects, but Sean's current DataCamp preference is a unified per-course folder
for active course work.

When in doubt, ask before deciding.

Do not touch Study_bubbles engine unless the engine is actually broken.

Do not hand-edit generated StudyBubble outputs.

Do not overbuild.

Artifact role map:

```text
Accumulated Field Guide
= whole-course memory map, navigation hub, and cross-chapter synthesis

Chapter Field Guides
= deep searchable teaching books for individual chapters

Quick Lookup
= smallest useful syntax and problem finder

Lab Run Book / Lab Guide
= hands-on plan plus evidence of what was actually practiced

Bill of Materials
= coverage inventory

Source Material
= raw evidence
```

---

## Codex behavior

When giving Codex prompts, treat Codex as Codex Low.

Codex should:

```text
- create or update files exactly as instructed
- avoid designing the curriculum independently
- avoid expanding scope
- avoid creating runnable labs unless explicitly instructed
- avoid touching Study_bubbles engine
- avoid hand-editing generated outputs
- report files changed and commands run
- keep changes scoped to the requested course folder
- ask or stop if source files are missing instead of inventing content
```

Git:

```text
Sean handles Git.
Codex may run scoped status checks only when useful.
Do not ask Codex to commit, stage, branch, or manage Git unless Sean asks.
```

---

## Fast-start instruction for a new course chat

Start by helping Sean process the course curriculum and video scripts.

Do not start with a giant build.

First, help create a fast Codex setup prompt that does the first setup pass in
as few iterations as possible:

```text
1. Create/verify the canonical course folder.
2. Save source material under source_material\.
3. Create/update Bill of Materials.
4. Create accumulated Field Guide Markdown skeleton.
5. Create accumulated Field Guide HTML overview using the standard dark style.
6. Create one lightweight HTML chapter-guide shell per course chapter.
7. Create one domain-specific Quick Lookup HTML skeleton.
8. Create course-local lab\ folder.
9. Create Lab Run Book / Lab Guide skeleton under lab\.
10. Copy or create setup SQL/code files under lab\ when source files are provided.
11. Update course index.html with links to all active artifacts.
12. Update session state.
```

Only split this into multiple Codex prompts if there is a real blocking reason.

The initial chapter pages and Quick Lookup should be shells, not fully expanded
books. Populate them during the live chapter pass.

If Sean's wording is vague, ask one short clarification question before writing
the Codex prompt.
