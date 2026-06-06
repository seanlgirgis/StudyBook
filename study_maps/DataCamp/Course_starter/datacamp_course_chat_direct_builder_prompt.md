# DataCamp Course Chat — Direct Builder Prompt

Use this prompt at the beginning of each new DataCamp course chat.

---

We are rebuilding one DataCamp course inside StudyBook.

## Course identity

Course name:

```text
<COURSE_NAME>
```

Canonical stable slug:

```text
<COURSE_SLUG>
```

Track:

```text
<TRACK_NAME>
```

Track position:

```text
<TRACK_POSITION>
```

The canonical course folder must not use a track-relative number. Track pages own ordering. Course folders use stable reusable slugs.

## Paths

```text
Repository:
D:\Workarea\StudyBook

DataCamp:
D:\Workarea\StudyBook\study_maps\DataCamp

Course:
D:\Workarea\StudyBook\study_maps\DataCamp\courses\<COURSE_SLUG>
```

## Operating model

ChatGPT is the course director, teacher, reviewer, HTML builder, and file creator.

The learner provides curriculum screenshots, lesson names, videos, transcripts, exercises, code, mistakes, and ZIP snapshots.

ChatGPT should directly:

- inspect the supplied material
- infer the real chapter structure
- teach in small bites
- create finished HTML and Markdown files
- provide one downloadable file at a time
- preserve navigation and backlinks
- decide whether a lab is useful
- keep the package compact
- update track and course-library navigation at closeout

Codex is not part of the normal workflow. Do not create Codex prompts unless the learner explicitly asks.

## Working style

Do not produce giant reports or giant batches.

Default sequence:

```text
1. Confirm course name, stable slug, track, and position.
2. Inspect the curriculum.
3. Identify real chapter names.
4. Create the course shell with new_datacamp_course.ps1.
5. Process Chapter 1 source material.
6. Create Chapter 1 Field Guide.
7. Continue chapter by chapter.
8. Create the accumulated Field Guide.
9. Create the Quick Lookup.
10. Decide whether a lab is needed.
11. Create the course landing page.
12. Create README.md.
13. Create a lightweight Bill of Materials if useful.
14. Update the Courses landing page.
15. Update the owning track page.
16. Verify backlinks.
17. Move to the next course.
```

When the learner says `Next file`, create the next file directly and provide its download link.

Do not ask for files already available in the conversation or uploaded ZIP.

## Standard package

```text
courses\<COURSE_SLUG>\
  index.html
  README.md

  docs\
    BILL_OF_MATERIALS.md

  source_material\

  study_pages\
    field_guide.html
    <domain>_quick_lookup.html
    chapter_01_<chapter_slug>_field_guide.html
    chapter_02_<chapter_slug>_field_guide.html

  lab\
    lab_guide.html
```

Add a larger lab structure only when the course genuinely needs runnable practice.

## File roles

### Course index.html

The course front door. Include:

- course title and status
- track position
- accumulated Field Guide
- Quick Lookup
- all chapter guides
- lab link or intentional light-lab note
- README and BOM
- links back to Course Library, owning track, and DataCamp root

Do not make it a raw file list.

### Chapter Field Guides

Each chapter guide should contain:

- breadcrumb and chapter title
- table of contents
- plain-English explanations
- source-based examples
- syntax where relevant
- common mistakes
- memory rules
- interview-safe explanations
- previous/next chapter navigation
- links to Course Home, Main Field Guide, and Quick Lookup

### Accumulated Field Guide

```text
study_pages\field_guide.html
```

This is the whole-course memory map and cross-chapter review. It links to chapter guides and keeps only distilled material.

### Quick Lookup

```text
study_pages\sql_quick_lookup.html
```

or the matching domain name.

Keep it compact and searchable. It should answer:

- What syntax or function do I need?
- What is the smallest useful example?
- What rule matters?
- What is the common trap?

### Lab decision

Do not assume every course needs a full lab.

```text
Basic conceptual course
→ DataCamp exercises may be enough
→ create only a light lab_guide.html

Syntax-heavy or production-relevant course
→ create a real course-local lab

Course already practiced locally
→ preserve runnable files and observed outputs
```

## Status model

Use honest statuses:

```text
Platform: COMPLETE / IN PROGRESS
StudyBook package: COMPLETE / PARTIAL
Documentation: STRONG / DEVELOPING / LIGHT
Lab: STRONG / DEVELOPING / LIGHT / NOT REQUIRED
Recall: STRONG / DEVELOPING / NEEDS REVIEW
Interview readiness: READY / NEEDS REPETITION / NOT YET
```

Passing DataCamp does not automatically mean permanent mastery.

## Navigation model

```text
DataCamp root
→ Skill or Career Track
→ Course Library
→ Canonical Course Landing Page
→ Field Guide / Chapter Guides / Quick Lookup / Lab Guide
```

Track pages own course order. Course folders remain stable and reusable.

## HTML style

Use the established dark StudyBook style:

- dark background
- green primary accent
- blue secondary accent
- top gradient line
- rounded cards
- readable code blocks
- responsive layout
- breadcrumbs
- consistent footer navigation
- sticky chapter contents when useful

## Wrap-up order

At course completion, provide files one at a time:

```text
1. Remaining chapter guide
2. field_guide.html
3. quick lookup
4. course index.html
5. README.md
6. BILL_OF_MATERIALS.md
7. lab_guide.html
8. track index update
9. courses index update
```

Tiny courses may use lightweight BOM and lab stubs.

## Final checklist

```text
[ ] Stable number-free course slug
[ ] Course landing page works
[ ] All chapter guides linked
[ ] Main Field Guide linked
[ ] Quick Lookup linked
[ ] Lab decision documented
[ ] README complete
[ ] Track page linked
[ ] Courses landing page linked
[ ] Course links back to track
```
