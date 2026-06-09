# Prompt Engineering with the OpenAI API — Field Guide

## Course status

- Platform: COMPLETE
- Documentation: STRONG
- Lab: STRONG
- Recall: DEVELOPING
- Interview readiness: NEEDS REPETITION

## Course map

1. [Chapter 1 — Introduction and Best Practices](chapter_01_introduction_to_prompt_engineering_best_practices_field_guide.html)
2. [Chapter 2 — Advanced Prompt Engineering Strategies](chapter_02_advanced_prompt_engineering_strategies_field_guide.html)
3. [Chapter 3 — Business Applications](chapter_03_prompt_engineering_for_business_applications_field_guide.html)
4. [Chapter 4 — Chatbot Development](chapter_04_prompt_engineering_for_chatbot_development_field_guide.html)
5. [Prompt Engineering Quick Lookup](sql_quick_lookup.html)

## Core model

```text
Goal
+ system behavior
+ trusted context
+ current request
+ examples and constraints
→ model output
→ deterministic validation
→ accept, retry, reject, or human review
```

## Main techniques

### Message roles

- **System:** persistent purpose, tone, domain, boundaries, fallback behavior, and small trusted context.
- **User:** current request and source material.
- **Assistant:** prior answer or demonstration of the desired behavior.

### Zero-shot, one-shot, and few-shot

- **Zero-shot:** instructions only.
- **One-shot:** one example teaches a format or mapping.
- **Few-shot:** several representative examples teach classes, style, or edge cases.

### Prompt structure

A dependable prompt normally contains:

1. task or role;
2. relevant context;
3. source boundaries or delimiters;
4. constraints and allowed values;
5. exact output structure;
6. missing-value or fallback behavior;
7. validation expectations.

### Delimiters

Use triple backticks or another clear boundary to separate instructions from source content. Delimiters improve readability and reduce ambiguity, but they are not a complete security boundary.

### Multi-step prompting

Use steps when later work depends on earlier work. Multiple output fields alone do not make a prompt multi-step.

### Reasoning and self-consistency

Ask for concise calculations or intermediate results when they aid inspection. Multiple candidate answers may expose alternatives, but agreement is not proof of correctness.

### Temperature

- Low temperature: stable extraction, classification, and formatting.
- Moderate temperature: broader hypotheses or creative alternatives.
- Temperature permits variation; the prompt controls the search space; evidence controls trust.

## Business transformations

- **Summarization:** compress while preserving the essential meaning.
- **Expansion:** elaborate wording without inventing facts or relationships.
- **Translation:** change language while preserving meaning, timing, and tone.
- **Tone adjustment:** change presentation without creating promises.
- **Proofreading:** fix grammar and punctuation without broad rewriting.
- **Classification:** choose from an explicit allowed label set.
- **Entity extraction:** return named fields using a fixed schema and null/N/A behavior.

## Machine-facing output

```text
unstructured text
→ constrained prompt
→ JSON
→ json.loads()
→ exact-key, type, value, and source validation
→ accepted record or controlled failure
```

Valid JSON is not automatically correct data.

## Chatbot development

A chatbot system prompt should define:

- purpose and domain;
- professional role;
- audience and tone;
- answer length and structure;
- allowed and disallowed behavior;
- exact fallback behavior;
- small trusted context when required.

### Context methods

- **System-prompt context:** compact reference for a small stable knowledge set.
- **Sample conversations:** teach both facts and conversational style.
- **Retrieval:** preferable for large or changing knowledge bases.

### Structured rolling state

```json
{
  "confirmed_facts": [],
  "recommended_actions": [],
  "completed_actions": [],
  "open_questions": []
}
```

Keep facts separate from recommendations. Let the model propose updates, but validate before storage.

## Common traps

1. Vague prompts produce hard-to-test output.
2. Examples with inconsistent labels teach inconsistency.
3. Expansion and tone rewriting can invent claims or commitments.
4. Context can constrain output without guaranteeing exact wording.
5. Model-generated JSON can be structurally valid but factually wrong.
6. Recycled summaries can accumulate memory drift.
7. A fluent answer is not a validated answer.

## Interview-safe summary

> I design prompts as explicit contracts: role, context, task, constraints, output schema, and fallback behavior. For production use, I parse and validate model output in deterministic code, and for chatbots I combine a persistent system contract with recent turns and compact structured state.
