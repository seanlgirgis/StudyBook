# 03c_text_normalization

## What This POC Does
This POC reads chunk records from `03b_chunk_documents`, normalizes the chunk text for simple lexical retrieval prep, validates records with Pydantic, and writes normalized chunk output.

## Input File
This POC consumes:

`..\03b_chunk_documents\outputs\chunked_documents.json`

## Output File
This POC creates:

`outputs\normalized_chunks.json`

## Fields Preserved and Added
For every input chunk, this POC preserves these fields exactly:
- `chunk_id`
- `document_id`
- `source_file`
- `source_path`
- `title`
- `chunk_index`
- `text`
- `character_count`

It then adds:
- `normalized_text`
- `normalized_character_count`

## Normalization Rules (Version 1)
- Unicode normalization to stable form (`NFKC`)
- Smart quotes/apostrophes mapped to plain quote/apostrophe where practical
- Long dashes converted to spaces
- Lowercasing
- Non-word punctuation replaced with spaces
- Repeated whitespace collapsed to single spaces
- Leading/trailing whitespace stripped

This POC intentionally does not:
- stem words
- remove stop words
- remove numbers
- modify original `text`
- overwrite chunk IDs

## Special Business-Term Handling
To make HVAC wording easier to search consistently:
- `A/C` and `a/c` normalize to `ac`
- `air-conditioning` normalizes to `air conditioning`
- `air conditioning` remains `air conditioning`

This is intentionally simple for learning. Larger synonym logic is out of scope here.

## Run Instructions
Run from repo root with environment bootstrap:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1
python .\pocs\03c_text_normalization\src\normalize_text.py
pytest -v .\pocs\03c_text_normalization\tests
```

## What Success Looks Like
- Script prints:
  - input path
  - output path
  - number of chunks read
  - number of chunks written
  - small before/after sample
- `outputs\normalized_chunks.json` exists and has one output record per input chunk
- Tests pass

## Explicitly Out Of Scope
This POC does not build TF-IDF indexing, search, embeddings, FastAPI, Docker, AWS resources, or integrated app behavior.
