# 03a_load_documents

## Purpose
Read synthetic markdown docs from pocs/02_fake_business_docs and turn them into Pydantic SourceDocument objects.

## What This Tiny POC Teaches
How to discover document files, parse markdown as raw text, and create typed document records with source metadata.

## Input Files
Markdown files from pocs/02_fake_business_docs/data/home_services_demo/*.md

## Expected Outputs
A validated in-memory list (and optional JSON preview later) of SourceDocument records.

## Command (Planned)
`powershell
python -m src.load_documents
`

## What Is Intentionally Not Included Yet
No chunking, no indexing, no scoring, no retrieval decisions.

## Retrieval Ladder Fit
Stage 1 of retrieval ladder: creates reliable typed source inputs for all later stages.
