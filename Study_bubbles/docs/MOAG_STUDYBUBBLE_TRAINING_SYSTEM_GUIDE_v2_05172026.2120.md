# MOAG StudyBubble Training System Guide v2

## Purpose

This is the master operating guide for creating a complete topic-training
system with StudyBubble and GenAI agents.

This guide is not only about bubble maps.

It governs the full learning product:

```text
study_maps/   = learning product, deployable study package, maps, course home,
                study pages, interview/rehearsal pages, glossary, safety notes

tutorials/    = hands-on lab bench, runnable code, commands, expected outputs,
                lab setup, lab troubleshooting

Study_bubbles/ = engine only
scripts/       = shared commands only
```

Use this guide when creating a learning topic such as Terraform, Power BI,
AWS, Kubernetes, OpenTelemetry, SQL, Python, Tableau, Databricks, or any other
StudyBook subject.

The main promise:

```text
Information in one place.
Hands-on in another place.
Engine separate from both.
```

---

## The Non-Negotiable Architecture Promise

Every learning topic must keep these domains separate.

```text
study_maps/**/<Topic>/
= the learning product
= the deployable study package
= primary course front door
= StudyBubble visual maps
= topic source JSON and layouts
= generated map outputs
= course navigation
= concept study pages
= interview Q&A
= flashcards
= glossary
= safety notes
= checklists
= diagrams and learning assets
= non-runnable conceptual examples
= session state and audit docs
```

```text
tutorials/**/<Topic>/
= the lab bench
= runnable labs
= code exercises
= command walkthroughs
= expected outputs
= lab setup
= lab troubleshooting
= provider downloads and temporary lab artifacts
= prompts for creating/running labs
```

```text
Study_bubbles/
= engine, viewer, builder, tests, schemas
= never a real topic content home
```

```text
scripts/
= shared StudyBook commands
= no per-topic script zoo
```

If an item is primarily for reading, studying, navigating, interviewing, or
rehearsing, it belongs under `study_maps`.

If an item is primarily for running commands, writing code, producing outputs,
or troubleshooting a lab, it belongs under `tutorials`.

If an item changes how StudyBubble itself builds, renders, syncs, validates, or
navigates, it belongs in `Study_bubbles`.

---

## Why This Guide Exists

A previous Terraform course build exposed a serious architecture smell:
course home pages, Q&A, flashcards, study pages, and conceptual material were
allowed to drift into `tutorials/`.

That violated the learner promise.

The corrected rule is now permanent:

```text
study_maps = study product and deployable knowledge package
tutorials  = lab bench and hands-on execution area
```

Do not weaken this rule in future projects.

---

## Core Operating Rule

```text
Teach first.
Design second.
Implement third.
Validate fourth.
Only debug the engine when the engine is actually broken.
```

Expanded:

1. Teach the concept simply.
2. Explain why it matters.
3. Propose the next small learning cluster.
4. Define the study-map and training-material placement.
5. Ask before writing files unless the user explicitly requested file changes.
6. Build/test only after implementation.
7. Audit domain placement before calling the work complete.

Avoid:

```text
- dumping a full encyclopedia
- syntax-first learning
- giant 50-node maps
- putting course home under tutorials
- putting Q&A or flashcards under tutorials
- putting runnable lab artifacts under study_maps
- hand-editing generated map outputs
- changing StudyBubble engine code for normal content work
```

---

## Roles and Responsibilities

### ChatGPT / Advisor Role

ChatGPT is the curriculum director, teacher, and reviewer.

Responsibilities:

```text
- teach the learner one concept at a time
- protect the learning sequence from overload
- define concept clusters
- define safe interview language
- review architecture decisions
- decide whether content belongs in study_maps or tutorials
- create precise Codex prompts
- audit Codex results
- prevent overclaiming experience
- prevent misplaced materials
```

ChatGPT should not behave like a blind follower. It should challenge bad
structure, unclear scope, and content sprawl.

### Codex / Agentic Builder Role

Codex is the local file executor.

Responsibilities:

```text
- create/update files from strict instructions
- preserve folder-domain boundaries
- run builds/tests/validations
- report files changed and commands run
- avoid inventing project structure
- avoid moving files without explicit reason
- avoid touching generated files directly
- avoid engine changes unless debugging is explicitly requested
```

### Learner Role

The learner studies, tests the workflow, gives feedback, and approves the next
cluster.

Responsibilities:

```text
- open the course front door
- click/read maps and study cards
- try labs only when ready
- report confusion or bad navigation
- approve implementation steps when needed
```

---

## Standard Folder Model

A mature topic should look like this.

```text
StudyBook/
  Study_bubbles/
    viewer/
    src/
    tools/
    tests/

  scripts/
    bubbles.ps1

  study_maps/
    <Category>/
      <Topic>/
        index.html
        README.md
        bubbles.ini
        STUDYBUBBLE_SESSION_STATE.md

        topics/
          *.studybubble.json

        layouts/
          *.layout.json

        outputs/
          *.html

        assets/
          images/
          diagrams/
          css/

        course/
          interview_qanda.html
          flashcards.html
          safety_notes.html
          glossary.html
          checklists/
          interview/
          rehearsal/

        study_pages/
          00_intro/
          01_big_picture/
          02_concept_deep_dive/

        docs/
          ARCHITECTURE_DECISIONS.md
          FINAL_ARCHITECTURE_AUDIT.md
          CONTENT_PLACEMENT_AUDIT.md

  tutorials/
    <Category>/
      <Topic>/
        index.html
        README.md

        01_first_lab/
          index.html
          README.md
          main.tf
          variables.tf
          outputs.tf
          expected_output/
          troubleshooting.md

        02_second_lab/
          index.html
          README.md
          src/
          expected_output/
          troubleshooting.md

        labs/
          shared_examples/

        prompts/
          create_lab_prompt.md
```

---

## Primary Opening Rule

The primary opening for a learning topic must live under `study_maps`.

Example:

```text
D:\Workarea\StudyBook\study_maps\IaC\TerraForm\index.html
```

This is the course front door.

It may link to:

```text
outputs/*.html                         StudyBubble map outputs
course/interview_qanda.html            Interview cockpit
course/flashcards.html                 Rehearsal cards
course/glossary.html                   Glossary
study_pages/**/index.html              Deeper non-runnable study pages
../../../tutorials/<Category>/<Topic>/ Lab hub only
```

The tutorials index is not the main study front door.

The tutorials index is the lab hub.

Example:

```text
D:\Workarea\StudyBook\tutorials\IaC\TerraForm\index.html
```

This page should say clearly:

```text
This folder is for hands-on labs and runnable examples.
The main study front door is under study_maps.
```

---

## File Placement Decision Tree

Use this before creating or moving any file.

### Put it in `study_maps/**/<Topic>/` if it is:

```text
- course home / front door
- study navigation page
- StudyBubble topic JSON
- StudyBubble layout JSON
- generated StudyBubble map output
- learning image or concept diagram
- conceptual explanation
- non-runnable study page
- glossary
- checklist
- safety notes
- interview Q&A
- flashcards
- rehearsal page
- curriculum state
- architecture decision
- final audit report
- map-level resource
- conceptual example that is not meant to run
```

### Put it in `tutorials/**/<Topic>/` if it is:

```text
- runnable lab
- lab README
- lab leader HTML
- main.tf / variables.tf / outputs.tf / provider files
- Python/SQL/YAML/etc. exercise code
- command transcript
- expected output
- troubleshooting for a lab
- setup needed to run a lab
- lab-specific prompt
- generated lab artifact
- temporary provider/cache/output folder
```

### Put it in `Study_bubbles/` only if it is:

```text
- viewer code
- builder code
- validator code
- schema code
- engine tests
- engine demo fixtures
- engine documentation
```

### Put it in `scripts/` only if it is:

```text
- shared StudyBook command
- reusable wrapper used across topics
```

---

## Red Flags: Stop and Reclassify

Stop before implementation if an agent proposes any of these:

```text
- tutorials/<Topic>/index.html as the primary course home
- tutorials/<Topic>/interview_qanda.html
- tutorials/<Topic>/flashcards.html
- tutorials/<Topic>/glossary.html
- tutorials/<Topic>/study_pages/
- tutorials/<Topic>/00_big_picture with no lab
- study_maps/<Topic>/main.tf
- study_maps/<Topic>/.terraform/
- study_maps/<Topic>/terraform.tfstate
- Study_bubbles/topics/<real-topic>.studybubble.json
- Study_bubbles/outputs/single_file/<real-topic>.html
- per-topic scripts/ folder copied into the topic
```

Default correction:

```text
Study/rehearsal/navigation material -> study_maps
Runnable lab material -> tutorials
Engine material -> Study_bubbles
Shared commands -> scripts
```

---

## Learning Material Layers

A topic-training system has multiple layers.

```text
Layer 1: Course Front Door
  study_maps/<Category>/<Topic>/index.html
  The dashboard for the whole learning product.

Layer 2: StudyBubble Maps
  study_maps/<Category>/<Topic>/outputs/*.html
  Visual concept islands and relationship maps.

Layer 3: Bubble Study Cards
  Stored in topic JSON; displayed in map side panel.
  Short definitions, examples, safe sentences, traps, and links.

Layer 4: Study Pages
  study_maps/<Category>/<Topic>/study_pages/**
  Longer non-runnable explanations and concept deep dives.

Layer 5: Rehearsal Material
  study_maps/<Category>/<Topic>/course/**
  Interview Q&A, flashcards, safety notes, glossary, checklists.

Layer 6: Hands-On Labs
  tutorials/<Category>/<Topic>/**
  Runnable code, commands, expected output, troubleshooting.
```

The rule:

```text
Maps help memory.
Study pages deepen understanding.
Rehearsal pages prepare speech.
Labs build practical confidence.
```

---

## Course Front Door Requirements

Every serious topic should have:

```text
study_maps/<Category>/<Topic>/index.html
```

This page should include:

```text
- topic title and purpose
- start-here path
- recommended study order
- links to all StudyBubble outputs
- links to study pages
- links to interview/rehearsal materials
- link to tutorials lab hub
- safety notes or overclaim guardrails when relevant
- next recommended work
```

It must not be placed under `tutorials`.

It must be deployable with the rest of the `study_maps` package.

---

## Tutorials Lab Hub Requirements

Every topic with labs may have:

```text
tutorials/<Category>/<Topic>/index.html
```

This page should include only:

```text
- lab setup instructions
- lab list
- prerequisites
- commands to run labs
- expected outputs
- cleanup warnings
- troubleshooting links
- link back to study_maps front door
```

It must not become the main course home.

It must not host Q&A, flashcards, glossary, or broad study pages.

---

## StudyBubble Topic JSON Standards

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
example
example.language
example.code
example.whatToNotice
mapResources
```

Bubble card rules:

```text
- teach quickly
- keep definitions short
- include safe interview language when helpful
- include common traps when useful
- include short examples only
- link to deeper material instead of crowding the card
```

Do not place full tutorials or long command transcripts inside a bubble card.

---

## Bubble Links vs Map Resources

Use bubble-specific links when the link explains the selected bubble.

Examples:

```text
Provider bubble -> Provider and Resource Lab
State bubble    -> State and Backend Lab
Plan bubble     -> Core Workflow Plan section
```

Use top-level `mapResources` when the link supports the whole map.

Examples:

```text
Open Course Home
Open Full Study Page
Open Hands-On Lab
Back to Parent Map
Next Map
Open Glossary
Open Interview Q&A
Open Flashcards
```

Course-home links in mapResources should point to the local study front door:

```json
{
  "label": "Open Course Home",
  "type": "course",
  "href": "../index.html"
}
```

Do not point course-home resources to `tutorials/<Topic>/index.html`.

Lab links may point to tutorials:

```json
{
  "label": "Open Hands-On Lab",
  "type": "lab",
  "href": "../../../../tutorials/IaC/TerraForm/02_core_workflow/index.html"
}
```

---

## Map Size and Learning Flow

Mandatory:

```text
Work one cluster at a time.
Keep each map focused.
Prefer 7 to 15 bubbles.
Hard maximum: 21 bubbles.
Split large topics into child maps.
```

Learning growth model:

```text
bubble -> cluster -> island -> course -> training system
```

Do not build the whole universe in one pass.

Suggested sequence:

```text
1. 1000-foot view
2. job/career relevance
3. core workflow
4. risk/safety/state
5. core building blocks
6. reuse/patterns
7. environments/team workflows
8. domain-specific examples
9. interview/rehearsal
10. hands-on labs
```

---

## Teaching Workflow

Use this sequence in every learning session:

```text
1. Tell the learner what to open.
2. Teach the concept in plain English.
3. Tell them what bubble or page to click.
4. Give one short thing to read or notice.
5. Ask for a plain-English explanation back.
6. Tighten their answer into interview-safe language.
7. Move to the next small step.
```

Do not start with syntax overload.

Do not ask the learner to run labs before they understand the concept.

---

## Implementation Workflow

When the user asks to implement:

```text
1. Confirm target category/topic path.
2. Define the front door under study_maps.
3. Define the lab hub under tutorials only if labs exist.
4. Create/update topic JSON and layouts under study_maps.
5. Create/update study pages under study_maps.
6. Create/update rehearsal pages under study_maps/course.
7. Create/update labs under tutorials.
8. Build maps from the active container.
9. Validate links and folder placement.
10. Write/update session state and audit docs.
```

Do not implement by scattering content across folders without an audit.

---

## Build and Layout Workflow

Initialize the StudyBook shell if needed:

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
```

Build from the active StudyBubble container:

```powershell
cd D:\Workarea\StudyBook\study_maps\<Category>\<Topic>
bubbles build
```

Sync layout from the active container:

```powershell
bubbles sync-layout
bubbles build
```

The container root is the folder containing `bubbles.ini`.

Do not teach users to count folder levels with commands like:

```powershell
..\..\scripts\bubbles.ps1 build
```

That is a fallback/debug pattern only.

---

## Generated Files Rule

Do not hand-edit generated HTML.

Generated files:

```text
study_maps/<Category>/<Topic>/outputs/*.html
Study_bubbles/outputs/single_file/*.html
```

Source files:

```text
study_maps/<Category>/<Topic>/topics/*.studybubble.json
study_maps/<Category>/<Topic>/layouts/*.layout.json
study_maps/<Category>/<Topic>/index.html
study_maps/<Category>/<Topic>/course/**
study_maps/<Category>/<Topic>/study_pages/**
study_maps/<Category>/<Topic>/assets/**
tutorials/<Category>/<Topic>/**
```

Edit source files, then rebuild.

---

## Acceptance Checklist: Course Architecture

A topic is not architecturally clean until all checks pass.

```text
[ ] study_maps/<Category>/<Topic>/index.html exists.
[ ] That index.html is the primary opening path.
[ ] tutorials/<Category>/<Topic>/index.html, if present, is lab-only.
[ ] Q&A lives under study_maps, not tutorials.
[ ] Flashcards live under study_maps, not tutorials.
[ ] Glossary/checklists/safety notes live under study_maps, not tutorials.
[ ] Non-runnable study pages live under study_maps, not tutorials.
[ ] Runnable labs live under tutorials, not study_maps.
[ ] No .tfstate, .terraform, provider cache, or expected lab output lives under study_maps.
[ ] Course-home mapResources point to ../index.html or another local study_maps path.
[ ] True lab links point to tutorials.
[ ] Generated outputs were rebuilt after topic JSON changes.
[ ] No real topic artifacts were written under Study_bubbles topics/ or outputs/.
[ ] README and session state document the architecture.
[ ] A final audit document exists for mature courses.
```

---

## Acceptance Checklist: StudyBubble Container

A StudyBubble visual-map container passes when:

```text
[ ] bubbles.ini exists in the active container root.
[ ] default_topic matches a real topic file under topics/.
[ ] topic JSON exists under topics/.
[ ] generated HTML is written under outputs/.
[ ] layout JSON is written under layouts/.
[ ] map opens directly in browser.
[ ] map is not a flat row by default.
[ ] group colors are visible.
[ ] group filter buttons match bubble colors.
[ ] system buttons remain neutral.
[ ] drag/export/sync-layout/rebuild preserves positions.
[ ] mapResources render separately from selected bubble details.
```

---

## Acceptance Checklist: Lab Bench

A tutorials lab bench passes when:

```text
[ ] tutorials/<Category>/<Topic>/index.html is labeled as labs/hands-on only.
[ ] README points back to the study_maps front door.
[ ] top-level tutorial folders are runnable labs or lab-support folders.
[ ] non-lab conceptual folders are absent.
[ ] Q&A and flashcards are absent.
[ ] study_pages is absent.
[ ] expected_output is inside lab folders only.
[ ] setup/troubleshooting material is lab-specific.
```

---

## Final Architecture Audit

For any mature course, create:

```text
study_maps/<Category>/<Topic>/docs/FINAL_ARCHITECTURE_AUDIT.md
```

It must include:

```text
- final primary opening path
- what lives in study_maps
- what lives in tutorials
- moved/copied files
- old links removed
- generated outputs rebuilt
- validation commands run
- remaining manual-review items
```

Search validations should include:

```text
- old course-home links to tutorials index: count must be 0
- Q&A/flashcards under tutorials: count must be 0
- study_pages under tutorials: count must be 0
- .tfstate/.terraform under study_maps: count must be 0
```

---

## Standard Codex Prompt: New Topic Training System

Use this when starting a new topic.

```text
We are creating a StudyBubble-based training system for <TOPIC>.

This is a training and learning system, not just a bubble map.

Non-negotiable architecture:

study_maps/<Category>/<Topic>
= learning product / deployable study package / course front door / maps /
  study pages / interview Q&A / flashcards / glossary / safety notes /
  conceptual non-runnable material.

tutorials/<Category>/<Topic>
= hands-on lab bench only / runnable code / commands / expected output /
  lab setup / lab troubleshooting.

Study_bubbles
= engine only.

Do not place the course home under tutorials.
Do not place Q&A, flashcards, glossary, safety notes, or study pages under
 tutorials.
Do not place runnable lab artifacts under study_maps.
Do not modify the StudyBubble engine unless something is actually broken.
Do not hand-edit generated outputs/*.html.

Start in teaching-first mode.

Before writing files:
1. Teach the 1000-foot concept.
2. Propose the first 5-10 bubble cluster.
3. Propose the course front door structure.
4. Propose what belongs in study_maps vs tutorials.
5. Wait for approval.

After approval, create or verify:

study_maps/<Category>/<Topic>/
  index.html
  README.md
  bubbles.ini
  STUDYBUBBLE_SESSION_STATE.md
  topics/
  layouts/
  outputs/
  assets/
  course/
  study_pages/
  docs/

tutorials/<Category>/<Topic>/
  index.html only if labs exist
  README.md only if labs exist
  lab folders only if runnable labs exist

Build from the active StudyBubble container:

cd D:\Workarea\StudyBook
.\env_setter.ps1
cd D:\Workarea\StudyBook\study_maps\<Category>\<Topic>
bubbles build

Final report must include:
- files created/changed
- what lives in study_maps
- what lives in tutorials
- commands run
- build result
- placement audit result
- final opening path
```

---

## Standard Codex Prompt: Architecture Audit

Use this before declaring a course complete.

```text
Run an architecture audit for <TOPIC>.

Rules:
study_maps/<Category>/<Topic> = study product.
tutorials/<Category>/<Topic> = lab bench only.
Study_bubbles = engine only.

Check for misplaced items.

Find and report:
1. Any course-home links pointing to tutorials/<Topic>/index.html.
2. Any Q&A, flashcards, glossary, safety notes, checklists, or study_pages
   under tutorials.
3. Any runnable lab artifacts under study_maps, including .tfstate,
   .terraform, provider downloads, expected_output, command logs, or main.tf.
4. Any real topic content under Study_bubbles/topics or
   Study_bubbles/outputs/single_file.
5. Any generated outputs that are stale compared to topic JSON.
6. Any broken links between study_maps and tutorials.

Do not change files in the first pass.

Final response:
- misplaced study items
- misplaced lab items
- stale links
- recommended fixes
- whether a repair pass is required
```

---

## Standard Codex Prompt: Repair Misplaced Material

Use this after an audit finds misplaced files.

```text
Repair misplaced material for <TOPIC>.

Rules:
study_maps/<Category>/<Topic> = learning product.
tutorials/<Category>/<Topic> = lab bench only.
Study_bubbles = engine only.

Move study/rehearsal/navigation material to study_maps.
Move runnable labs/code/expected outputs to tutorials.
Do not delete until replacement paths and links are verified.
Do not hand-edit generated outputs; rebuild them.
Do not modify StudyBubble engine unless something is actually broken.

Required steps:
1. Move/copy files to correct domain.
2. Update study_maps index.html.
3. Update tutorials index/README to lab-only.
4. Update topic JSON mapResources and externalLinks.
5. Rebuild outputs from active container.
6. Search for old/bad links.
7. Validate the final opening path.
8. Create/update FINAL_ARCHITECTURE_AUDIT.md.

Final response:
- files moved
- files changed
- links updated
- commands run
- build result
- validation counts
- remaining manual-review items
- final opening path
```

---

## When To Return To StudyBubble Engine Work

Only return to engine work for actual engine/tooling failures:

```text
- build failure
- viewer bug
- layout sync problem
- broken image handling
- navigation issue
- mapResources not rendering
- serious console error
- wrong output location caused by tooling
- wrong layout location caused by tooling
- stable command failure from valid container
```

Do not return to engine work because topic content needs improvement.

Do not return to engine work because a map needs better teaching.

Do not return to engine work because files were placed in the wrong topic
folder. Fix the project architecture first.

---

## Minimum Handoff Packet

When moving to another AI session, provide:

```text
- this MOAG Training System Guide v2
- topic curriculum state if it exists
- STUDYBUBBLE_SESSION_STATE.md
- current topic JSON files
- current layout JSON files
- study_maps index.html
- tutorials index.html if labs exist
- architecture audit if mature course exists
- known build/sync/link issues
- final opening path
```

---

## Final Law

```text
StudyBubble is the visual learning engine.
scripts/bubbles.ps1 is the shared command layer.
study_maps/**/<Topic> is the learning product.
tutorials/**/<Topic> is the hands-on lab bench.
Study_bubbles is the engine, not the topic home.
The folder containing bubbles.ini is the active StudyBubble container.
Course home belongs under study_maps.
Q&A, flashcards, glossary, safety notes, and study pages belong under study_maps.
Runnable labs, code exercises, expected outputs, and lab troubleshooting belong
under tutorials.
Generated outputs are never hand-edited.
Learning sessions teach first and implement only when asked.
Engine work happens only when the tool breaks.
Before declaring success, run a placement audit.
Information in one place. Hands-on in another place.
```
