# 03b_chunk_documents

## Purpose
Split loaded docs into smaller searchable chunks with metadata.

## What This Tiny POC Teaches
How chunk size and overlap affect retrieval granularity and citation readiness.

## Input Files
SourceDocument objects from 03a_load_documents output.

## Expected Outputs
ChunkDocument records with chunk_id, source_id, offsets, and text.

## Command (Planned)
`powershell
python -m src.chunk_documents
`

## What Is Intentionally Not Included Yet
No ranking model, no typo handling, no answer generation.

## Retrieval Ladder Fit
Stage 2: prepares retrieval-ready chunks for vectorless lexical baselines.
