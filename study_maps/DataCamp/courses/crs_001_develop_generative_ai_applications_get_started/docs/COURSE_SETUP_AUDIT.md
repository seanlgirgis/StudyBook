# Course Setup Audit

## Course identity

- Course: **Develop Generative AI Applications: Get Started**
- Platform: Coursera
- Provider: IBM
- Program: RAG for Generative AI Applications Specialization
- Position: Course 1 of 4
- Canonical library ID: `crs_001`
- Canonical slug: `crs_001_develop_generative_ai_applications_get_started`
- Canonical path:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\crs_001_develop_generative_ai_applications_get_started
```

## Architecture audit

- [x] Canonical course folder established under `DataCamp\courses`
- [x] Coursera `crs_` prefix preserved
- [x] Stable three-digit library number added
- [x] Existing DataCamp course folders left unchanged
- [x] Single canonical course home used
- [x] Course root contains `index.html` and `README.md`
- [x] Theory and study material stored under `study_pages`
- [x] Runnable Python examples stored under `lab\python`
- [x] Source evidence separated under `source_material`
- [x] Inventory and audit files stored under `docs`
- [x] Relative links used inside the course package
- [x] Duplicate skill-track-contained course copy treated as legacy rather than canonical

## Study-page audit

- [x] Main accumulated Field Guide created from the approved template
- [x] Module 1 field guide completed
- [x] Module 2 field guide completed
- [x] Module 3 field guide completed
- [x] Multiline code blocks corrected in all module guides
- [x] Concept and Code Quick Lookup created
- [x] LangChain Code Patterns guide created
- [x] Markdown companion guides created
- [x] Learning evidence page created
- [x] Certification review digest created
- [x] Certification self-test created
- [x] No unresolved template placeholders remain in delivered HTML
- [x] Module previous/next navigation added
- [x] Main Field Guide links to all three module guides

## Lab audit

- [x] Existing starter code normalized under `lab\python`
- [x] 17 Python examples preserved
- [x] All 17 Python files passed syntax compilation
- [x] `lab\README.md` created
- [x] `lab\00_how_to_run.md` created
- [x] `lab\lab_run_book.md` created
- [x] `lab\lab_guide.html` created
- [x] Troubleshooting notes created
- [x] Source ZIP archived under `lab\source_archive`
- [ ] Successful runtime outputs saved under `lab\expected_outputs`
- [ ] Module 3 Flask application lab completed and recorded

## Learning evidence audit

Validated locally:

- PromptTemplate with one variable
- PromptTemplate with several variables
- ChatPromptTemplate with system and human roles
- FewShotPromptTemplate
- LCEL local-function pipeline
- OpenAI LCEL pipeline
- IBM watsonx smallest test
- OpenAI and watsonx provider-switching comparison
- RunnableParallel
- JsonOutputParser
- Provider-native Pydantic structured output
- MessagesPlaceholder
- Manual history growth
- Reusable chat function with history
- RunnableWithMessageHistory legacy example

Important observed corrections:

- `prompt.invoke()` prepares a prompt
- `model.invoke()` generates a response
- `chain.invoke()` runs the complete pipeline
- provider-neutral structure does not guarantee identical provider behavior
- `LCEL` required full LangChain context to avoid acronym ambiguity
- `JsonOutputParser` returned a `dict`
- provider-native structured output returned a validated Pydantic object
- `RunnableWithMessageHistory` is deprecated and retained only as enrichment

## Navigation audit

- [x] Course root index links to the Main Field Guide
- [x] Course root index links to all three module guides
- [x] Course root index links to the Quick Lookup
- [x] Course root index links to the Lab Run Book
- [x] Course root index links to documentation files
- [x] Module guides link to Course Home
- [x] Module guides link to the Main Field Guide
- [x] Module guides link to the Quick Lookup
- [x] Module previous/next links are present
- [ ] Coursera specialization page updated to canonical numbered course path
- [ ] General Course Library page updated to canonical numbered course path
- [ ] Legacy skill-track-contained copy removed or replaced with a redirect

## Honest status

```text
Platform: IN PROGRESS
StudyBook package: STRONG / PARTIAL
Documentation: STRONG
Lab: STRONG for Modules 1–2
Module 3 Flask lab: PENDING
Recall: DEVELOPING
Interview readiness: NEEDS REPETITION
```

## Remaining closeout work

1. Complete the remaining official Coursera lessons and exercises.
2. Complete and record the Module 3 Flask application lab.
3. Save representative successful outputs under `lab\expected_outputs`.
4. Update the specialization page.
5. Update the central Course Library page.
6. Reconcile final platform completion and mastery status.
7. Decide whether to remove or redirect the legacy course copy under the specialization folder.
