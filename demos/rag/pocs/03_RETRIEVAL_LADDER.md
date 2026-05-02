# Milestone 3 Retrieval Ladder Overview

## Why Split Retrieval Into Tiny POCs
Breaking retrieval into small, testable stages reduces confusion, makes debugging easier, and prevents architectural jumps before fundamentals are understood.

## Index-Time vs Query-Time
- Index-time: load, structure, and chunk document corpus before customer questions arrive.
- Query-time: normalize user text, score against indexed chunks, then decide retrieve/clarify/fallback.

## Why Start Local Before LLMs
A local deterministic baseline makes failures observable and repeatable. It helps us learn retrieval quality independent of model behavior.

## Why TF-IDF Is A Useful Baseline
TF-IDF is fast, explainable, and easy to inspect. It provides a practical lexical baseline before semantic or model-based retrieval upgrades.

## Why Typo Handling Matters
Real customer text is noisy. Character-level retrieval improves resilience for misspellings like "coolng", "untis", "financng", and "diagnstic".

## Why Ambiguity Should Trigger Clarification
Low-confidence or ambiguous matches should request clarification instead of forcing a wrong answer. This improves trust and reduces unsafe guidance.

## Reuse Path Into Integrated App
These ladder stages are designed to become reusable classes/modules later:
- document loading and chunking utilities
- query normalization utilities
- word/char/hybrid retrievers
- retrieval decision policy layer
- retrieval evaluation harness

That progression supports later integration in the production-oriented app without skipping learning steps.
