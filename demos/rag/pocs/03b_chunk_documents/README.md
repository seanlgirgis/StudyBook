# 03b_chunk_documents

## What This POC Does
This POC reads loaded source documents from `03a_load_documents`, splits each document into smaller text chunks, validates each chunk with Pydantic, and writes a structured chunk output JSON file.

This is an educational preparation step for later retrieval stages.

## Input File
This POC consumes:

`..\03a_load_documents\outputs\loaded_documents.json`

From the `03b_chunk_documents` folder, that path points to the `03a` output file.

## Output File
This POC creates:

`outputs\chunked_documents.json`

## What Chunking Means
Chunking means breaking a large document into smaller pieces of text.  
Each chunk is small enough to be handled efficiently by later retrieval methods.

## Why RAG Systems Chunk Documents
RAG systems usually retrieve small relevant passages, not full documents.  
Chunking improves precision by giving retrieval systems better-sized search units.

## Why Chunking Happens Before TF-IDF/Search/Embeddings
Before ranking or vector methods can work, documents must be normalized into consistent units.  
Chunking is that preparation layer: it creates the retrieval units that TF-IDF, keyword search, or embeddings can score later.

## Chunking Strategy In This POC
- Target chunk size: `800` characters
- Overlap: `100` characters
- Paragraph-aware split preference:
  - prefer splitting at paragraph boundaries (`\n\n`) when possible
  - fall back to a hard character split when needed

Overlap helps preserve context across chunk boundaries for later retrieval quality.

## Metadata Preserved On Each Chunk
Each `DocumentChunk` preserves:
- `chunk_id`
- `document_id`
- `source_file`
- `source_path`
- `title`
- `chunk_index`
- `text`
- `character_count`

Preserving metadata keeps every chunk traceable to its original source document for future citations.

## What `chunk_id` Means
`chunk_id` is a stable identifier for each chunk:

`{document_id}__chunk_{chunk_index:03d}`

Example:
- `hvac_repair_policy__chunk_000`
- `hvac_repair_policy__chunk_001`

## How `chunk_index` Works
`chunk_index` resets to `0` for each new document and increments by `1` for each additional chunk in that same document.

## What `character_count` Validates
`character_count` must always equal `len(text)`.  
Pydantic validation enforces this so chunk payloads are internally consistent.

## Run Instructions
Run from this folder with environment bootstrap:

```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\03b_chunk_documents
. D:\Workarea\StudyBook\env_setter.ps1
python .\src\chunk_documents.py
pytest -v
```

## What Success Looks Like
- Script prints:
  - input path
  - output path
  - number of input documents
  - number of chunks created
  - average chunks per document
- `outputs\chunked_documents.json` exists and contains chunk records
- `pytest -v` passes

## Explicitly Out Of Scope
This POC does not perform search.  
This POC does not build a TF-IDF index.  
This POC does not create embeddings.  
This POC does not answer user questions.  
This POC only prepares document chunks for later retrieval steps.
