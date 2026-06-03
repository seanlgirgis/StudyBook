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

Canonical tutorial/lab folder pattern:

```text
D:\Workarea\StudyBook\tutorials\DataCamp\courses\<course_slug>
```

Preferred temporary source handoff folder:

```text
D:\Users\shareuser\Downloads
```

Use relative paths in documentation whenever possible.

## Fast course workflow agreement

For each DataCamp course, avoid many tiny setup iterations.

Use this faster order:

```text
1. Capture curriculum + transcript/source files.
2. Create Bill of Materials.
3. Create Field Guide Markdown.
4. Create Field Guide HTML cheat sheet using the standard dark style.
5. Create Lab Run Book skeleton.
6. Start live DataCamp exercises.
7. Patch Field Guide and Lab Run Book during the live pass.
```

The setup goal is speed, not perfection.

Do not spend many rounds polishing setup artifacts before learning.

## Phase 1 — Capture source material

I will provide some or all of these:

```text
1. Course curriculum / outline image
2. Course outline text
3. Video scripts or transcripts
4. Exercise prompts, screenshots, or notes
```

Raw source material belongs under:

```text
study_maps\DataCamp\courses\<course_slug>\source_material\
```

Raw source material is evidence. Do not treat it as final study material.

When a source file is provided through Downloads, Codex should:

```text
1. Read the source file from D:\Users\shareuser\Downloads.
2. Copy the useful content into the course source_material folder.
3. Archive the consumed source file under the course source_material\archive folder.
4. Confirm the Downloads copy no longer exists.
5. If moving fails, do not delete the file; report the issue.
```

## Phase 2 — Build Artifact 1: Bill of Materials

Create the Bill of Materials before writing the Field Guide.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\docs\BILL_OF_MATERIALS.md
```

The Bill of Materials should include:

```text
- course title
- canonical slug
- source inventory
- curriculum image status
- transcript status
- exercise notes status
- chapter list
- lesson/video list
- topic list
- function/command/operator list
- data type list
- SQL/Python/etc. pattern list as applicable
- field guide targets
- lab run book targets
- fast-review topics
- slow-down topics
- interview-important topics
- open questions / missing material
```

This is the inventory. It should be concise but useful.

## Phase 3 — Build Artifact 2: Field Guide Markdown

Create the Field Guide Markdown under the course study folder.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\field_guide.md
```

The Field Guide is the knowledge book for the course.

It should include:

```text
- all major course ideas
- plain-English explanations
- syntax patterns
- generic code samples
- DataCamp-style exercise patterns
- common mistakes and corrections
- interview questions and answers
- job/interview translation
- quick memory nuggets
- common traps and edge cases
- when to use each function, command, or pattern
```

The Field Guide belongs under `study_maps`, not `tutorials`.

## Phase 4 — Build Artifact 3: Field Guide HTML Cheat Sheet

Create an HTML cheat sheet from the Field Guide.

Preferred file:

```text
study_maps\DataCamp\courses\<course_slug>\study_pages\field_guide.html
```

This is the browser cheat sheet I will keep open while doing DataCamp and labs.

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

Each course should have its own title, badge, table of contents, and sections.

## Phase 5 — Build Artifact 4: Lab Run Book

Create a Lab Run Book under the course tutorial/lab folder.

Preferred file:

```text
tutorials\DataCamp\courses\<course_slug>\lab_run_book.md
```

The Lab Run Book is the hands-on practice plan.

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
- future runnable file plan
```

Runnable practice belongs under `tutorials`, not `study_maps`.

For the first pass, create a skeleton only.
Do not create SQL files, Docker files, datasets, or expected outputs unless I explicitly ask.

## Phase 6 — Live DataCamp pass

After the Bill of Materials, Field Guide, HTML cheat sheet, and Lab Run Book skeleton exist, we go through the DataCamp course.

During the live course pass, capture:

```text
- missing examples
- DataCamp-specific wording
- exercise mistakes
- tricky syntax
- shortcuts
- confusion points
- useful additions to the Field Guide
- useful additions to the Lab Run Book
```

The live DataCamp pass is the validation and gap-filling pass.

## Teaching style

Teach me in small bites.

When I paste my answer or SQL/code:

```text
1. Comment on my solution first.
2. Tell me what is right.
3. Point out the exact issue if something is wrong.
4. Give a small hint before dumping the answer.
5. Give corrected SQL/code only when needed.
6. Capture reusable patterns and mistakes.
```

Every 5–10 meaningful learning interactions, recommend a small StudyBook/Codex documentation update.

## Architecture rules

Follow MOAG / StudyBook boundaries:

```text
study_maps = learning product, BOM, Field Guide, HTML cheat sheet, notes,
             maps, Q&A, flashcards, source transcripts, session state

tutorials  = runnable labs, Lab Run Book, SQL files, code, expected outputs,
             lab troubleshooting

Study_bubbles = engine only

scripts = shared commands only
```

Do not put study material under tutorials.

Do not put runnable lab artifacts under study_maps.

Do not touch Study_bubbles engine unless the engine is actually broken.

Do not hand-edit generated StudyBubble outputs.

Do not overbuild.

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
```

Git:

```text
Sean handles Git.
Codex may run scoped status checks only when useful.
Do not ask Codex to commit, stage, branch, or manage Git unless Sean asks.
```

## Fast-start instruction for this chat

Start by helping me process the course curriculum and video scripts.

Do not start with a giant build.

First, help me create a fast Codex setup prompt that does the first setup pass in as few iterations as possible:

```text
1. Create/verify the course folder.
2. Save source material.
3. Create/update Bill of Materials.
4. Create Field Guide Markdown.
5. Create Field Guide HTML using the standard dark style.
6. Create Lab Run Book skeleton.
7. Update session state.
```

Only split this into multiple Codex prompts if there is a real blocking reason.
