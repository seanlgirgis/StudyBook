# Prompt Engineering with the OpenAI API

Canonical DataCamp course package for the **Developing AI Applications** skill track.

## Course identity

- Canonical slug: `prompt_engineering_with_the_openai_api`
- Track position: 4
- Platform status: **PASSED**
- Documentation coverage: **COMPLETE**
- Lab coverage: **STRONG**
- Recall confidence: **DEVELOPING**
- Interview readiness: **NEEDS REPETITION**

## Course scope

This course covers four connected areas:

1. **Introduction and best practices**
   - system, user, and assistant roles
   - clear instructions and constraints
   - delimiters and f-strings
   - structured and conditional output

2. **Advanced prompting strategies**
   - zero-shot, one-shot, and few-shot prompting
   - multi-step prompting
   - brief reasoning patterns
   - self-consistency
   - temperature and variation

3. **Business applications**
   - summarization and expansion
   - translation, tone adjustment, and proofreading
   - classification and entity extraction
   - JSON output, parsing, and deterministic validation
   - AI-assisted text-to-structure pipelines

4. **Chatbot development**
   - dual-prompt helpers
   - purpose, role, tone, and domain boundaries
   - external context and sample conversations
   - stateful chat
   - structured rolling memory
   - application-side state validation

## Recommended study order

1. `study_pages/field_guide.html`
2. `study_pages/chapter_01_introduction_to_prompt_engineering_best_practices_field_guide.html`
3. `study_pages/chapter_02_advanced_prompt_engineering_strategies_field_guide.html`
4. `study_pages/chapter_03_prompt_engineering_for_business_applications_field_guide.html`
5. `study_pages/chapter_04_prompt_engineering_for_chatbot_development_field_guide.html`
6. `study_pages/sql_quick_lookup.html`
7. `lab/lab_run_book.md`
8. Chapter lab READMEs and Python files in numerical order

## Main artifacts

```text
index.html
README.md
STUDYBUBBLE_SESSION_STATE.md

docs/
  BILL_OF_MATERIALS.md
  COURSE_SETUP_AUDIT.md

study_pages/
  field_guide.md
  field_guide.html
  chapter_01_introduction_to_prompt_engineering_best_practices_field_guide.html
  chapter_02_advanced_prompt_engineering_strategies_field_guide.html
  chapter_03_prompt_engineering_for_business_applications_field_guide.html
  chapter_04_prompt_engineering_for_chatbot_development_field_guide.html
  sql_quick_lookup.html

lab/
  00_how_to_run.md
  lab_run_book.md
  chapter_01/
  chapter_02/
  chapter_03/
  chapter_04/
  openai_support/
```

## Reusable architecture

The local `openai_support` package separates API integration from prompt-study code:

```text
Message
→ represents one role/content message

RequestOptions
→ carries model-request options

OpenAIService
→ sends requests and returns response text

chapter exercise
→ focuses on the functional prompting lesson
```

## Strongest course lessons

```text
Instructions define the allowed behavior.
Examples demonstrate the desired pattern.
Delimiters separate instructions from input data.
Schemas make output easier to validate.
Temperature permits variation but does not guarantee useful diversity.
Valid JSON is not automatically correct data.
The model proposes; deterministic code validates.
A chatbot system prompt is an operating contract.
Context grounds an answer but does not guarantee exact source fidelity.
Structured state is safer than a continuously rewritten free-form memory.
```

## Closeout status

The platform course and four chapter study passes are complete. The course remains in review mode.

Remaining enhancement work:

- create `study_pages/prompt_engineering_pattern_dictionary.html`;
- create a final self-test / certification-prep page;
- add links to those materials after creation;
- update the DataCamp courses index and the Developing AI Applications track page.

## Canonical path

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\prompt_engineering_with_the_openai_api
```
