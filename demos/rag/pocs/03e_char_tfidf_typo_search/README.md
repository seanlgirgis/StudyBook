# 03e_char_tfidf_typo_search

## Purpose
Use character-level TF-IDF to handle misspellings like coolng, untis, financng, diagnstic.

## What This Tiny POC Teaches
How character n-grams recover relevance under noisy or misspelled queries.

## Input Files
Possibly misspelled customer queries and existing chunk corpus.

## Expected Outputs
Top-k typo-resilient matches with char-level scores.

## Command (Planned)
`powershell
python -m src.char_tfidf_typo_retrieval
`

## What Is Intentionally Not Included Yet
No word+char fusion and no policy decision logic yet.

## Retrieval Ladder Fit
Stage 5: adds robust typo handling for realistic customer input.
