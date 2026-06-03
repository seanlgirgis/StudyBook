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

Use relative paths in documentation whenever possible.

## Our course workflow agreement

For each DataCamp course, we will work in this order:

### Phase 1 — Capture source material first

I will provide:

```text
1. Course curriculum / outline
2. Video scripts or transcripts
3. Exercise prompts, screenshots, or notes when useful
```

Store raw source material under:

```text
source_material/
```

Raw material is evidence. Do not treat it as final study material.

### Phase 2 — Build Artifact 1: Field Guide

Create a field guide under the course study folder.

Preferred file:

```text
study_pages/field_guide.md
```

The field guide is the knowledge book for the course.

It should include:

```text
- all major course ideas
- plain-English explanations
- SQL/Python/etc. syntax patterns as applicable
- generic code samples
- DataCamp-style exercise patterns
- common mistakes and corrections
- interview questions and answers
- job/interview translation
- quick memory nuggets
- common traps and edge cases
- when to use each function, command, or pattern
```

The field guide belongs under `study_maps`, not `tutorials`.

### Phase 3 — Build Artifact 2: Lab Run Book

Create a lab run book under the course tutorial/lab folder.

Preferred file:

```text
tutorials/DataCamp/courses/<course_slug>/lab_run_book.md
```

The lab run book is the hands-on practice plan.

It should include:

```text
- lab purpose
- sample dataset design
- table schemas or input data design
- seed data ideas
- exercises
- expected outputs
- practice checkpoints
- troubleshooting notes
- chapter-by-chapter lab path
```

Runnable practice belongs under `tutorials`, not `study_maps`.

### Phase 4 — Go through DataCamp course live

After the field guide and lab run book exist, we go through the DataCamp course.

During the live course pass, capture:

```text
- missing examples
- DataCamp-specific wording
- exercise mistakes
- tricky syntax
- shortcuts
- confusion points
- useful fillers for the field guide
- useful fillers for the lab run book
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

Every 5–10 meaningful learning interactions, remind me to update
StudyBook/Codex documentation.

## Architecture rules

Follow MOAG / StudyBook boundaries:

```text
study_maps = learning product, field guide, notes, maps, Q&A, flashcards
tutorials  = runnable labs, lab run book, SQL files, code, expected outputs
Study_bubbles = engine only
scripts = shared commands only
```

Do not put study material under tutorials.

Do not put runnable lab artifacts under study_maps.

Do not touch Study_bubbles engine unless the engine is actually broken.

Do not hand-edit generated outputs.

Do not overbuild.

## Codex behavior

When giving Codex prompts, treat Codex as Codex Low.

Codex should:

```text
- create or update files exactly as instructed
- avoid designing the curriculum independently
- avoid expanding scope
- avoid creating labs unless explicitly instructed
- avoid touching Study_bubbles engine
- avoid hand-editing generated outputs
- report files changed and commands run
```

## First task for this chat

Start by helping me process the course curriculum and video scripts.

Do not start with a giant build.

First, help me organize the source material and propose the initial field guide
and lab run book structure for this course.
