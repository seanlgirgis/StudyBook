# 03a_load_documents

## Purpose
Read synthetic markdown docs from pocs/02_fake_business_docs and turn them into Pydantic SourceDocument objects.

## What This Tiny POC Teaches
How to discover markdown files on disk, validate structured document records with Pydantic, and export clean JSON for downstream retrieval steps.

## Input Files
`D:\Workarea\StudyBook\demos\rag\pocs\02_fake_business_docs\data\home_services_demo\*.md`

## Expected Outputs
`D:\Workarea\StudyBook\demos\rag\pocs\03a_load_documents\outputs\loaded_documents.json`

## Commands To Run
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\03a_load_documents
python .\src\load_documents.py
pytest -v
```

## Expected Runtime Output
- Script summary with docs directory, markdown count, output path, and source file names.
- `loaded_documents.json` containing 16 validated `SourceDocument` records.
- Passing pytest suite.

## What Is Intentionally Not Included
- No chunking
- No TF-IDF or scoring
- No retrieval decisioning
- No answer generation
- No AI calls

## Retrieval Ladder Fit
Stage 1 of retrieval ladder: creates reliable typed source inputs for all later stages.

## Next POC
`03b_chunk_documents`
