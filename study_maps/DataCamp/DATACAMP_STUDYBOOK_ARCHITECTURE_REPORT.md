# DataCamp StudyBook Architecture Report

Prepared: 2026-06-07

## Purpose

This report explains how the DataCamp learning system is structured inside StudyBook today, how courses and projects are created, how landing pages and reusable components are organized, and how courses/projects connect into tracks and then back up into the general DataCamp landing pages.

This is written as a handoff document for starting or expanding a new DataCamp study track.

## Canonical root

Primary working root:

```text
D:\Workarea\StudyBook\study_maps\DataCamp
```

Main top-level folders:

```text
study_maps\DataCamp\
|-- index.html
|-- README.md
|-- DATACAMP_STUDYBOOK_ARCHITECTURE_REPORT.md
|-- assets\
|-- docs\
|-- Course_starter\
|-- courses\
|-- projects\
|-- skill_tracks\
|-- career_tracks\
|-- Archive\
```

## Core architecture rule

The architecture is built around one central rule:

- Tracks own ordering.
- Courses and projects are canonical reusable packages.
- Course folders must use stable slugs, not track-relative numbering.
- The same course can appear in more than one track without duplicating the course package.

This rule is repeated across:

- `README.md`
- `docs/ARCHITECTURE_DECISIONS.md`
- `index.html`
- `Course_starter/datacamp_course_startup_agreement_prompt.md`
- `Course_starter/datacamp_course_chat_direct_builder_prompt.md`
- `new_datacamp_course.ps1`

## Navigation model

The intended navigation hierarchy is:

```text
DataCamp root
-> Skill track or career track
-> Ordered track items
-> Canonical course or project landing page
-> Course/project study artifacts
```

Concrete page map:

```text
index.html
|-- courses/index.html
|   |-- courses/<course_slug>/index.html
|   |   |-- study_pages/field_guide.html
|   |   |-- study_pages/chapter_*_field_guide.html
|   |   |-- study_pages/*quick_lookup*.html
|   |   |-- lab/*
|   |   |-- docs/*
|   |   `-- source_material/*
|-- projects/index.html
|   `-- projects/<project_slug>/index.html
|       |-- study_pages/project_field_guide.html
|       |-- study_pages/sql_quick_lookup.html
|       |-- lab/*
|       |-- docs/*
|       `-- source_material/*
|-- skill_tracks/index.html
|   `-- skill_tracks/<track_slug>/index.html
`-- career_tracks/index.html
    `-- career_tracks/<track_slug>/index.html
```

## General DataCamp landing pages

### 1. DataCamp root landing page

File:

```text
index.html
```

Role:

- Front door for the whole DataCamp StudyBook area.
- Highlights the current active skill track.
- Highlights a related career track.
- Highlights a model canonical course package.
- Links into course, project, skill-track, and career-track libraries.

Main page components:

- Hero banner
- Primary action buttons
- Primary Tracks section
- Model Course Package section
- Libraries section
- Legacy note

### 2. Course library landing page

File:

```text
courses/index.html
```

Role:

- Canonical course catalog.
- Lists reusable course packages independent of track position.
- Shows summary metadata for each course.
- Links back to tracks and DataCamp home.

Course-library card components:

- Completion badge
- Track context badge
- Course title
- Short course summary
- Metadata lines
- Canonical relative path
- Open-course link

### 3. Project library landing page

File:

```text
projects/index.html
```

Role:

- Canonical project catalog.
- Lists completed reusable project packages.
- Links back to DataCamp home, course library, and track pages.

Project-library card components:

- Project title
- Short problem statement
- Pill badges for domain/status/lab
- Open-project link

### 4. Skill-track landing pages

Files:

```text
skill_tracks/index.html
skill_tracks/<track_slug>/index.html
```

Role:

- Own the learning order.
- Point to canonical courses and projects.
- Contain track-level progress, sequence, and related navigation.

Important distinction:

- `skill_tracks/index.html` is mostly a library of track entries.
- `skill_tracks/01_sql_fundamentals/index.html` is the current best example of a fully connected track page.
- Most other skill-track pages are placeholders.

### 5. Career-track landing pages

Files:

```text
career_tracks/index.html
career_tracks/<track_slug>/index.html
```

Role:

- Higher-level role path pages.
- Meant to reuse the same canonical courses and projects.
- Currently mostly placeholders.

## Course package contract

The canonical course contract is centered on:

```text
courses\<course_slug>\
```

Representative package:

```text
courses\functions_for_manipulating_data_in_postgresql\
|-- index.html
|-- README.md
|-- STUDYBUBBLE_SESSION_STATE.md
|-- docs\
|   |-- BILL_OF_MATERIALS.md
|   `-- COURSE_SETUP_AUDIT.md
|-- source_material\
|   |-- README.md
|   |-- course_curriculum_outline.md
|   |-- transcript_raw_combined.md
|   |-- exercise_notes.md
|   `-- archive\
|-- study_pages\
|   |-- field_guide.md
|   |-- field_guide.html
|   |-- chapter_01_..._field_guide.html
|   |-- chapter_02_..._field_guide.html
|   |-- chapter_03_..._field_guide.html
|   |-- chapter_04_..._field_guide.html
|   `-- sql_function_quick_lookup.html
`-- lab\
    |-- README.md
    |-- 00_how_to_run.md
    |-- lab_run_book.md
    |-- lab_guide.html
    |-- expected_outputs\
    |-- notes\
    `-- sql\
```

### What each course component does

`index.html`

- Course landing page.
- Main navigation hub for the package.
- Shows status, study order, chapter links, resources, lab links, and closeout notes.

`README.md`

- Human-readable package summary.
- Quick folder map and usage explanation.

`STUDYBUBBLE_SESSION_STATE.md`

- Session continuity artifact when used.
- Tracks working state rather than acting as the main study content.

`docs/BILL_OF_MATERIALS.md`

- Coverage inventory.
- Tracks chapter list, sources, planned artifacts, topic scope, and missing items.

`docs/COURSE_SETUP_AUDIT.md`

- Audit/checklist for course setup completeness.
- Confirms artifact presence and validation status.

`source_material/`

- Raw evidence layer.
- Holds curriculum outlines, transcripts, PDFs, screenshots, exercise notes, and archives.
- Should not be treated as the final polished study layer.

`study_pages/field_guide.md`

- Whole-course memory map in Markdown.

`study_pages/field_guide.html`

- Whole-course browser study guide.
- Distilled cross-chapter reference and navigation hub.

`study_pages/chapter_*_field_guide.html`

- Deep chapter-level guides.
- Each one is a searchable teaching page for one course chapter.

`study_pages/*quick_lookup*.html`

- Compact searchable syntax/pattern page.
- Optimized for fast retrieval while studying or practicing.

`lab/`

- Hands-on layer.
- Holds run instructions, SQL/code files, troubleshooting notes, expected outputs, and practice evidence.

## Course landing page components

The course landing page pattern is standardized by `Course_starter/course_index_template.html`.

Main components on a canonical course page:

- Breadcrumbs
- Hero section
- Course summary paragraph
- Action buttons
- Five-status dashboard
- Recommended study order section
- Chapter Guides section
- Course Resources section
- Local Lab section
- Course Closeout section
- Footer navigation

Current status fields used on live course pages:

- Platform status
- Documentation coverage
- Lab coverage
- Recall confidence
- Interview readiness

## Field Guide component system

The page system for course study pages is standardized by these starter templates:

```text
Course_starter/field_guide_template.html
Course_starter/section_field_guide_template.html
Course_starter/sql_quick_lookup_template.html
```

### Accumulated Field Guide page structure

Typical components:

- Breadcrumbs
- Hero section
- Status cards
- Sticky table of contents
- Chapter-guide cards
- Big-picture section
- Core concepts grid
- Syntax/pattern blocks
- Comparisons and decision tables
- Common mistakes
- Interview translation
- Local lab evidence
- Memory nuggets
- Footer

### Chapter Field Guide page structure

Typical components:

- Breadcrumbs
- Hero section
- Backlinks to course home, main field guide, and quick lookup
- Sticky section table of contents
- Big-picture section
- Concept cards
- Worked examples
- Validation and troubleshooting
- Common mistakes
- Interview translation
- Memory review
- Next-section navigation

### Quick Lookup page structure

Typical components:

- Breadcrumbs
- Hero section
- Search box
- Lookup-card grids
- Tiny syntax examples
- Trap callouts
- Compact reference diagram/callout

## Project package contract

The canonical project contract is centered on:

```text
projects\<project_slug>\
```

Representative package:

```text
projects\analyzing_students_mental_health\
|-- index.html
|-- README.md
|-- docs\
|   `-- PROJECT_SETUP_AUDIT.md
|-- source_material\
|   |-- README.md
|   `-- students.csv
|-- study_pages\
|   |-- project_field_guide.html
|   `-- sql_quick_lookup.html
`-- lab\
    |-- lab_guide.html
    |-- expected_outputs\
    |-- notes\
    `-- sql\
```

### What each project component does

`index.html`

- Project front door.
- Explains the problem, study order, runnable files, validated results, and navigation.

`study_pages/project_field_guide.html`

- Project-specific deep explanation page.
- Covers dataset meaning, logic, final query, findings, traps, and interview translation.

`study_pages/sql_quick_lookup.html`

- Compact project SQL retrieval page.

`lab/lab_guide.html`

- Step-by-step local reconstruction guide.

`lab/sql/*.sql`

- Runnable project evidence.
- Typically includes table creation, load step, accepted solution, and practice queries.

`docs/PROJECT_SETUP_AUDIT.md`

- Completeness and validation audit for the project package.

## How courses are created

There are two main creation mechanisms in the repo.

### 1. Scripted scaffold

Primary script:

```text
new_datacamp_course.ps1
```

This script creates:

- canonical course folder
- `docs`, `source_material`, `study_pages`, and `lab` subfolders
- `index.html`
- `README.md`
- `docs/BILL_OF_MATERIALS.md`
- `source_material/README.md`
- `study_pages/field_guide.html`
- chapter guide HTML stubs
- quick lookup HTML stub
- `lab/lab_guide.html`

Key script inputs:

- `CourseName`
- `CourseSlug`
- `TrackName`
- `TrackPosition`
- `Chapters`
- `QuickLookupName`

Important script behavior:

- protects existing files unless `-Force` is used
- slug must be lowercase snake_case
- chapter files are auto-named with `chapter_XX_<slug>_field_guide.html`

### 2. Prompt + template workflow

Starter assets:

```text
Course_starter/datacamp_course_startup_agreement_prompt.md
Course_starter/datacamp_course_chat_direct_builder_prompt.md
Course_starter/course_index_template.html
Course_starter/field_guide_template.html
Course_starter/section_field_guide_template.html
Course_starter/sql_quick_lookup_template.html
```

This is the higher-level design workflow for building a richer final course package after the basic shell exists.

The documented fast workflow is:

1. Capture curriculum and source files.
2. Create/update the Bill of Materials.
3. Create the accumulated Field Guide Markdown skeleton.
4. Create the accumulated Field Guide HTML page.
5. Create lightweight chapter-guide shells.
6. Create the quick lookup page.
7. Create the local lab folder and run book.
8. Add SQL/code practice files if needed.
9. Study the live course.
10. Update chapter pages, quick lookup, and lab evidence during the live pass.
11. Reconcile the full package at closeout.

## How projects are created

Primary script:

```text
new_datacamp_project.ps1
```

This script creates:

- canonical project folder
- `docs`, `source_material`, `study_pages`, and `lab` subfolders
- `index.html`
- `README.md`
- `docs/PROJECT_SETUP_AUDIT.md`
- `study_pages/project_field_guide.html`
- `study_pages/sql_quick_lookup.html`
- `lab/lab_guide.html`
- starter SQL files
- troubleshooting and expected-output folders

Key project inputs:

- `ProjectName`
- `ProjectSlug`
- `SkillTrackName`
- `SkillTrackFolder`
- `QuickLookupName`

Important rule:

- The project page links back to the owning skill track, but the project package itself stays canonical and reusable.

## How tracks connect to courses and projects

### Skill tracks

Skill tracks are meant to be focused learning bundles.

Their responsibilities are:

- own track numbering/order
- mix course items and project items
- show rebuild/progress state
- link directly into canonical packages
- link onward to related tracks and the course library

Best current example:

```text
skill_tracks/01_sql_fundamentals/index.html
```

This page already links to:

- 7 canonical course packages
- 1 canonical project package
- a related career track
- the course library

It also keeps track-only items that are not yet built:

- bonus project
- assessment

### Career tracks

Career tracks are broader role-oriented paths.

Their intended responsibilities are:

- group multiple reusable courses/projects into a role path
- provide business/job framing
- reuse canonical assets instead of duplicating them

Current state:

- The career-track library exists.
- Individual career-track folders exist.
- Most career-track pages are placeholders and do not yet link to canonical course/project packages.

## How courses and projects connect back to general DataCamp pages

Canonical courses typically link upward to:

- DataCamp home
- Course Library
- at least one owning track page

Canonical projects typically link upward to:

- DataCamp home
- Projects index
- at least one owning skill track

Track pages typically link outward to:

- canonical course packages
- canonical project packages
- related tracks
- course library
- DataCamp home

So the connection model is bidirectional:

```text
DataCamp root <-> libraries <-> tracks <-> canonical packages
```

## Current inventory snapshot

### Canonical course folders currently present

```text
courses/data_manipulation_in_sql
courses/database_design
courses/functions_for_manipulating_data_in_postgresql
courses/intermediate_sql
courses/introduction_to_sql
courses/joining_data_in_sql
courses/postgresql_summary_stats_and_window_functions
```

Summary of current course-package completeness:

- All 7 current canonical course folders have `index.html`, `README.md`, `study_pages/field_guide.html`, a quick lookup page, a `lab` folder, and `docs/BILL_OF_MATERIALS.md`.
- 6 of 7 also have `docs/COURSE_SETUP_AUDIT.md`.
- `introduction_to_sql` is the only current canonical course missing `docs/COURSE_SETUP_AUDIT.md`.
- Most current canonical courses use 4 chapter field-guide pages.
- `introduction_to_sql` currently uses 2 chapter field-guide pages.

### Canonical project folders currently present

```text
projects/analyzing_students_mental_health
```

### Skill tracks currently present

- A fully connected `01_sql_fundamentals` track page exists.
- Many other skill-track folders exist as placeholders.

### Career tracks currently present

- 27 career-track folders exist.
- They are mostly placeholders today.

## Important current-state observations

These are especially useful for anyone starting the next track build.

### 1. The repo shows an architecture transition

Some older documentation says runnable labs remain in:

```text
tutorials\DataCamp
```

But the active course-building prompts and the actual canonical course packages now place the active lab inside:

```text
study_maps\DataCamp\courses\<course_slug>\lab\
```

For practical work, the unified per-course folder appears to be the current active model.

### 2. SQL Fundamentals is the strongest reference implementation

If a new track must be built, use these as the main examples:

- `skill_tracks/01_sql_fundamentals/index.html`
- `courses/functions_for_manipulating_data_in_postgresql/`
- `courses/database_design/`
- `projects/analyzing_students_mental_health/`

### 3. Track wiring is not complete across the whole system

Today:

- one skill track is strongly wired
- one project is wired into that skill track
- career tracks are mostly not yet wired into canonical course/project pages

### 4. Some status text is inconsistent

Examples:

- several completed course landing pages say `COMPLETE`
- some corresponding supporting docs like README or BOM still say `Under construction`
- many placeholder track pages still say `Under construction`

### 5. Placeholder naming cleanup is still needed

Current `skill_tracks` folders include duplicate numeric prefixes such as:

- `06_pandas_data_manipulation` and `06_python_data_manipulation`
- `07_data_cleaning` and `07_pandas_data_analysis`
- `08_data_cleaning` and `08_power_bi_fundamentals`
- `09_databricks_fundamentals` and `09_power_bi_fundamentals`
- `10_databricks_fundamentals` and `10_pyspark_fundamentals`
- `11_data_engineering_pipelines` and `11_pyspark_fundamentals`
- `12_ai_fundamentals_for_data_work` and `12_data_engineering_pipelines`

This means the placeholder track-numbering layer still needs reconciliation before it can be treated as finalized.

### 6. One broken career-track index link exists

`career_tracks/index.html` currently links to:

```text
28_java_developer/index.html
```

but that folder does not exist in `career_tracks/`.

## Recommended process for starting a new study track

If ChatGPT is asked to start the next DataCamp track, the safest workflow is:

1. Pick or create the track folder under `skill_tracks/` or `career_tracks/`.
2. Treat the track page as the owner of course/project ordering.
3. Do not number the canonical course folders.
4. For each missing course, scaffold or build `courses/<stable_slug>/`.
5. For each missing project, scaffold or build `projects/<stable_slug>/`.
6. Link the track page to those canonical packages.
7. Add backlinks from course/project pages to the owning track page.
8. Update `courses/index.html` and `projects/index.html` when a package becomes canonical.
9. Update `index.html` if the new track becomes a primary focus.

## Recommended creation checklist for a new canonical course

```text
[ ] Decide stable course slug
[ ] Create/verify canonical folder under courses/
[ ] Add source material under source_material/
[ ] Create/update BILL_OF_MATERIALS.md
[ ] Create field_guide.md
[ ] Create field_guide.html
[ ] Create chapter_XX_*_field_guide.html pages
[ ] Create quick lookup page
[ ] Create lab folder and run book
[ ] Create or import SQL/code practice files if needed
[ ] Build course index.html
[ ] Add backlinks to Course Library, DataCamp home, and owning track
[ ] Add course card to courses/index.html when canonical
[ ] Link course from owning track page
```

## Recommended creation checklist for a new canonical project

```text
[ ] Decide stable project slug
[ ] Create/verify canonical folder under projects/
[ ] Preserve raw dataset/instructions in source_material/
[ ] Create project field guide
[ ] Create SQL quick lookup
[ ] Create lab guide
[ ] Preserve runnable SQL/code in lab/sql/
[ ] Record validation evidence and expected outputs
[ ] Build project index.html
[ ] Add backlinks to Projects index, DataCamp home, and owning skill track
[ ] Add project card to projects/index.html when canonical
[ ] Link project from owning track page
```

## Best reference files for future work

Architecture and direction:

- `README.md`
- `docs/ARCHITECTURE_DECISIONS.md`
- `docs/MIGRATION_PLAN.md`
- `docs/MIGRATION_LOG.md`

Course-building workflow:

- `Course_starter/datacamp_course_startup_agreement_prompt.md`
- `Course_starter/datacamp_course_chat_direct_builder_prompt.md`
- `new_datacamp_course.ps1`
- `Course_starter/course_index_template.html`
- `Course_starter/field_guide_template.html`
- `Course_starter/section_field_guide_template.html`
- `Course_starter/sql_quick_lookup_template.html`

Project-building workflow:

- `new_datacamp_project.ps1`

Best live examples:

- `skill_tracks/01_sql_fundamentals/index.html`
- `courses/functions_for_manipulating_data_in_postgresql/index.html`
- `courses/database_design/index.html`
- `projects/analyzing_students_mental_health/index.html`

## Bottom line

The DataCamp StudyBook system is designed as a reusable package architecture:

- track pages are the playlists
- course pages are the reusable learning products
- project pages are the reusable practice products
- landing pages connect the whole system together

For the next track build, the safest strategy is to treat `01_sql_fundamentals` as the reference implementation, create new canonical course/project packages with stable slugs, and wire the new track page to those packages instead of duplicating content inside the track folder itself.
