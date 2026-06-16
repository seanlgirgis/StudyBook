# Codex Implementation Prompt — Course 1 Study System

Implement the local study system for Coursera Course 1:

**Develop Generative AI Applications: Get Started**

## Operating agreement

The user runs all commands and provider calls manually.

Codex performs file implementation only.

Do not run:

- Python examples;
- pytest;
- pip installation;
- Coursera labs;
- provider calls;
- Git commands.

Report every file created or modified.

## Target root

Create or update this exact course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\courses\develop_generative_ai_applications_get_started
```

If the folder already exists, inspect it first and preserve existing useful content.

Use only relative links inside Markdown and HTML.

Do not use absolute local paths inside navigation links.

## Source package supplied by the user

The user will provide the extracted contents of this planning package. Copy the supplied files into the target root while preserving their names and contents.

The package contains:

```text
README.md
course_01_map.md
course_01_study_guide.html
course_01_concept_index.html
examples_catalog.json
module_01_study_facts.md
module_02_study_facts.md
module_03_study_facts.md
lab_plan.md
requirements_course_reference.txt
starter_code/
```

## Create this final structure

```text
develop_generative_ai_applications_get_started/
├── README.md
├── index.html
├── course_01_map.md
├── course_01_study_guide.html
├── course_01_concept_index.html
├── examples_catalog.json
├── lab_plan.md
├── requirements_course_reference.txt
├── source_material/
│   ├── README.md
│   ├── module_01/
│   ├── module_02/
│   └── module_03/
├── study_pages/
│   ├── module_01_study_facts.md
│   ├── module_02_study_facts.md
│   └── module_03_study_facts.md
├── lab/
│   ├── README.md
│   ├── module_01/
│   │   ├── starter_code/
│   │   ├── coursera_lab/
│   │   └── notes/
│   ├── module_02/
│   │   ├── starter_code/
│   │   ├── coursera_lab/
│   │   └── notes/
│   └── module_03/
│       ├── starter_code/
│       ├── coursera_lab/
│       └── notes/
└── course_closeout/
    ├── course_01_code_patterns.md
    ├── course_01_self_test.md
    └── course_01_completion_summary.md
```

## File placement

Move or copy:

```text
module_01_study_facts.md
→ study_pages/module_01_study_facts.md

module_02_study_facts.md
→ study_pages/module_02_study_facts.md

module_03_study_facts.md
→ study_pages/module_03_study_facts.md
```

Copy all current `starter_code/*.py` into:

```text
lab/module_01/starter_code/
```

Do not put all future examples into Module 1. Module 2 and Module 3 starter-code folders remain ready for later work.

## Create `index.html`

Create a self-contained local landing page with no external dependencies.

It must link to:

- Course 1 map
- Visual study guide
- Searchable concept index
- Module 1 study facts
- Module 2 study facts
- Module 3 study facts
- Lab plan
- Module 1 starter code folder
- Module 2 lab folder
- Module 3 lab folder
- Course closeout folder

Use the same visual language as `course_01_study_guide.html`.

Show this learning sequence prominently:

```text
Map
→ concept bite
→ tiny example
→ Coursera lesson
→ Coursera lab
→ cleanup
```

## Create `source_material/README.md`

Use this content:

```markdown
# Source Material

Store user-provided Coursera transcripts, screenshots, lab instructions, and downloaded reference files here.

## Rules

- Preserve original source files.
- Do not rewrite transcripts in place.
- Put cleaned study notes in `study_pages/`.
- Put working code in `lab/`.
- Do not commit secrets or API keys.
- Keep Coursera-provided lab code separate from locally written starter examples.
```

## Create `lab/README.md`

Use this content:

```markdown
# Course 1 Lab Workspace

## Workflow

1. Review the module map.
2. Learn one concept in a small block.
3. Run the relevant starter example.
4. Open the Coursera lab.
5. Implement the lab together.
6. Copy the final clean code into `coursera_lab/`.
7. Record surprises and errors in `notes/`.

## Boundary

Starter examples explain one idea.

Coursera lab folders preserve the actual course work.

Do not turn starter examples into a production framework.
```

## Create closeout stubs

Create these as useful stubs, not empty files.

### `course_closeout/course_01_code_patterns.md`

Include headings:

```markdown
# Course 1 Code Patterns

## PromptTemplate
## ChatPromptTemplate
## MessagesPlaceholder
## FewShotPromptTemplate
## LCEL
## Output Parsers
## Provider Adapters
## Flask Integration
```

Under each heading write:

```text
To be completed after the related Coursera lab.
```

### `course_closeout/course_01_self_test.md`

Include sections:

- Concept questions
- Code reading
- Small coding tasks
- Application architecture
- Provider-neutral design
- Flask integration

Mark it as a course-end artifact.

### `course_closeout/course_01_completion_summary.md`

Include:

- Course status
- Modules completed
- Labs completed
- Quiz results
- New skills
- Reused Stage 1 foundation
- Remaining gaps
- Next course transition

## Update catalogs after placement

Update `examples_catalog.json`, `course_01_study_guide.html`, and `course_01_concept_index.html` only as needed so starter-code links point to:

```text
lab/module_01/starter_code/<filename>
```

The HTML must continue to work from `file://`.

Do not use `fetch()`.

## Environment guidance

Do not install packages.

Preserve `requirements_course_reference.txt` as a reference file.

Create no virtual environment automatically.

Add this note to `README.md`:

```markdown
## Environment Note

The package versions shown in Coursera may be older than the current local Python environment. Use a separate course virtual environment and validate compatibility before installing the reference versions.
```

## Accuracy and scope checks

Confirm:

- all HTML and Markdown links are relative;
- every linked file exists;
- JSON is valid;
- no transcript text is copied into generated answers beyond summarized study notes;
- no API key or secret is present;
- no numbered Stage 1 foundation brick is modified;
- no `rag_foundation` library file is modified;
- no tests are modified;
- no Git command is run.

## Final response format

Return:

```text
Course 1 study system implemented.

Files created:
- <full paths>

Files modified:
- <full paths>

Starter examples installed:
- <filenames>

Navigation:
- <landing page path>
- <study guide path>
- <concept index path>

Commands run:
- None. User will run validation manually.

Scope confirmation:
- No provider calls.
- No package installation.
- No Git operations.
- No Stage 1 foundation files modified.
```
