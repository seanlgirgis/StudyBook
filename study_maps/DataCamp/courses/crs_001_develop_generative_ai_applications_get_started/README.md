# Develop Generative AI Applications: Get Started

## Course identity

- Platform: Coursera
- Provider: IBM
- Program: RAG for Generative AI Applications Specialization
- Position: Course 1 of 4
- Canonical library ID: `crs_001`
- Canonical slug: `crs_001_develop_generative_ai_applications_get_started`
- Status: In progress

Canonical folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\crs_001_develop_generative_ai_applications_get_started
```

## Purpose

This course introduces the theory and implementation patterns needed to build a basic generative AI application.

The package is organized around four learning layers:

```text
Theory
→ understand the concepts

Code patterns
→ remember how to implement them

Labs
→ verify behavior locally

RemNote
→ reinforce recall over time
```

## Course modules

1. **Generative AI, Prompt Engineering, and Prompt Templates**
   - generative versus discriminative AI
   - foundation models and LLMs
   - zero-shot, one-shot, and few-shot prompting
   - self-consistency
   - `PromptTemplate`
   - `ChatPromptTemplate`
   - `FewShotPromptTemplate`

2. **Introduction to LangChain in Generative AI Applications**
   - LangChain components
   - LCEL
   - runnables and automatic coercion
   - `RunnableParallel`
   - output parsers
   - provider-native structured output
   - message history and provider switching

3. **Build a Generative AI Application with LangChain**
   - model selection and evaluation
   - multimodel design
   - Flask routing
   - HTTP responses and validation
   - prototype-to-production concerns

## Folder roles

```text
index.html
→ course front door

study_pages/
→ theory, module guides, quick lookup, code memory, review, and self-test

lab/
→ runnable Python examples, commands, outputs, and troubleshooting

source_material/
→ curriculum, transcript, screenshot, notebook, and exercise evidence

docs/
→ bill of materials and setup audit
```

## Main study pages

```text
study_pages/field_guide.html
study_pages/field_guide.md
study_pages/chapter_01_generative_ai_prompt_engineering_and_prompt_templates_field_guide.html
study_pages/chapter_02_introduction_to_langchain_in_generative_ai_applications_field_guide.html
study_pages/chapter_03_build_a_generative_ai_application_with_langchain_field_guide.html
study_pages/concept_and_code_quick_lookup.html
study_pages/langchain_code_patterns.html
study_pages/certification_review_digest.html
study_pages/certification_self_test.html
```

## Local lab

Runnable examples are stored under:

```text
lab/python/
```

The lab covers:

- prompt templates;
- chat prompt templates;
- few-shot prompts;
- local and provider-backed LCEL pipelines;
- OpenAI and IBM watsonx provider switching;
- `RunnableParallel`;
- JSON parsing;
- Pydantic structured output;
- `MessagesPlaceholder`;
- manual and reusable conversation history.

Start with:

```text
lab/00_how_to_run.md
lab/lab_run_book.md
lab/lab_guide.html
```

## Current status

```text
Platform: IN PROGRESS
Documentation: STRONG
Local lab: STRONG for Modules 1–2
Module 3 Flask lab: PENDING
Recall: DEVELOPING
Interview readiness: NEEDS REPETITION
```

## Recommended study order

1. Open `index.html`.
2. Read `study_pages/field_guide.html`.
3. Study the three module guides in order.
4. Use `concept_and_code_quick_lookup.html` for fast recall.
5. Practice with `langchain_code_patterns.html`.
6. Run the examples from `lab/python/`.
7. Review the RemNote theory and coding decks.
8. Return to Coursera and complete the official lessons and labs.
9. Reconcile new Coursera evidence into the course package.

## Architecture rule

This folder is the single canonical home for the course.

Specialization, certificate, and track pages should link here using relative links. They should not maintain duplicate active copies of this course.
