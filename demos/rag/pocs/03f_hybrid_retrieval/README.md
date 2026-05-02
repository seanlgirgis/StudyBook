# 03f_hybrid_retrieval

## Purpose
Combine word TF-IDF and character TF-IDF scores into one local hybrid retrieval baseline.

## What This Tiny POC Teaches
How score blending can outperform either retriever alone.

## Input Files
Word-level and char-level score outputs for same query/chunk set.

## Expected Outputs
Merged ranking with component scores and final blended score.

## Command (Planned)
`powershell
python -m src.hybrid_retrieval
`

## What Is Intentionally Not Included Yet
No answer generation and no production API integration.

## Retrieval Ladder Fit
Stage 6: creates practical local retrieval baseline for later RAG wiring.
