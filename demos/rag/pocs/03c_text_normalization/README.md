# 03c_text_normalization

## Purpose
Clean customer text, normalize domain terms, expand simple synonyms, and handle common typo patterns.

## What This Tiny POC Teaches
How normalization improves lexical retrieval consistency before scoring.

## Input Files
Raw customer query text and optional normalization dictionaries.

## Expected Outputs
Normalized query variants and trace metadata for what changed.

## Command (Planned)
`powershell
python -m src.normalize_text
`

## What Is Intentionally Not Included Yet
No retrieval scoring yet, no confidence thresholds yet.

## Retrieval Ladder Fit
Stage 3: improves query quality before indexing/search stages.
