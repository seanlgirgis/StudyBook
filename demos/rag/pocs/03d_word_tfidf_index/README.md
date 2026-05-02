# 03d_word_tfidf_index

## Purpose
Use scikit-learn word-level TF-IDF to retrieve relevant chunks for clean questions.

## What This Tiny POC Teaches
How word n-grams and cosine similarity create a fast baseline retriever.

## Input Files
Normalized query text and chunk corpus from earlier stages.

## Expected Outputs
Top-k chunk matches with similarity scores and source metadata.

## Command (Planned)
`powershell
python -m src.word_tfidf_retrieval
`

## What Is Intentionally Not Included Yet
No typo-specialized search and no hybrid weighting yet.

## Retrieval Ladder Fit
Stage 4: first working lexical retrieval baseline for clean input.
