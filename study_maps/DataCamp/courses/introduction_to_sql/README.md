# Introduction to SQL

Canonical DataCamp course package for:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\introduction_to_sql
```

## Course identity

- Course: Introduction to SQL
- Level: Basic
- DataCamp duration: approximately 2 hours
- Chapters: 2
- Track position: Course 1 in SQL Fundamentals
- Canonical slug: `introduction_to_sql`
- Platform status: Complete
- StudyBook status: Wrapped and ready for review

## Purpose

This course establishes the basic vocabulary and query patterns needed for later SQL courses.

It covers:

- relational databases
- tables, rows, columns, and records
- keys and unique identifiers
- data types
- database schemas
- servers and database systems
- `SELECT`
- `FROM`
- selecting one, several, or all columns
- SQL formatting
- `DISTINCT`
- aliases with `AS`
- views
- SQL flavors and dialects
- PostgreSQL `LIMIT`
- SQL Server `TOP`

## Primary opening page

Open:

```text
index.html
```

The course landing page links to the accumulated Field Guide, chapter guides, Quick Lookup, documentation, and track navigation.

## Course package structure

```text
introduction_to_sql/
├── index.html
├── README.md
├── docs/
│   └── BILL_OF_MATERIALS.md
├── lab/
│   └── lab_guide.html
├── source_material/
└── study_pages/
    ├── field_guide.html
    ├── sql_quick_lookup.html
    ├── chapter_01_relational_databases_field_guide.html
    └── chapter_02_querying_field_guide.html
```

## Study pages

### Accumulated Field Guide

```text
study_pages\field_guide.html
```

Role:

- whole-course memory map
- cross-chapter summary
- core syntax reference
- common mistakes
- interview translation
- final review

### Chapter 1

```text
study_pages\chapter_01_relational_databases_field_guide.html
```

Topics:

- databases
- relational organization
- tables
- rows and columns
- naming
- keys
- data types
- schemas
- servers

### Chapter 2

```text
study_pages\chapter_02_querying_field_guide.html
```

Topics:

- queries
- `SELECT`
- `FROM`
- multiple columns
- `SELECT *`
- SQL style
- `DISTINCT`
- aliases
- views
- SQL flavors
- `LIMIT`
- `TOP`

### SQL Quick Lookup

```text
study_pages\sql_quick_lookup.html
```

Role:

- compact searchable syntax reference
- smallest useful examples
- common traps
- quick interview answers

## Lab decision

A separate large lab package is not required for this course.

Reason:

- the course is introductory
- the DataCamp exercises already provide sufficient practice
- the main value is fast recall and correct vocabulary
- larger practical labs begin to matter more in later SQL courses

The existing file:

```text
lab\lab_guide.html
```

should document this decision and may contain only lightweight practice suggestions.

## Source material

The `source_material` folder is reserved for:

- course curriculum evidence
- raw transcripts
- lesson notes
- archived source videos or references
- exercise notes if needed

Raw source material should remain evidence, not final study material.

## Track relationship

This course belongs to:

```text
skill_tracks\01_sql_fundamentals
```

The track page owns the course number and sequence.

The canonical course folder does not include a track-relative number because the same course may appear in more than one track.

## Navigation rules

The main navigation path is:

```text
DataCamp index
→ SQL Fundamentals skill track
→ Introduction to SQL course landing page
→ Field Guide / Chapter Guides / Quick Lookup
```

All major HTML pages should link back to:

- the course home
- the main Field Guide
- related chapter pages where useful
- SQL Fundamentals
- DataCamp home where practical

## Completion summary

- Platform course: complete
- Chapter 1 guide: complete
- Chapter 2 guide: complete
- Accumulated Field Guide: complete
- SQL Quick Lookup: complete
- Course landing page: complete
- Lab requirement: intentionally light
- Track backlink: required from SQL Fundamentals
- Recommended next course: Intermediate SQL

## Maintenance rule

Treat this folder as the canonical active package.

Do not create numbered duplicates for track position.

Future improvements should be limited to:

- correcting factual or navigation issues
- adding useful exercise mistakes
- improving examples
- fixing broken relative links
- adding source evidence when needed

Do not expand this basic course into an oversized lab or documentation project.
