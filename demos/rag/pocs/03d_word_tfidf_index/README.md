# 03d_word_tfidf_index

## What This POC Does
This POC reads normalized chunk records from `03c_text_normalization`, validates them with Pydantic, builds a word-level TF-IDF catalog using scikit-learn, and saves reusable index artifacts for later retrieval stages.

## Input File
This POC consumes:

`..\03c_text_normalization\outputs\normalized_chunks.json`

## Output Files
This POC creates:

- `outputs\tfidf_index.joblib`
- `outputs\index_metadata.json`

## Why This Step Exists
This stage turns normalized text into a saved lexical catalog so later retrieval steps can rank chunks by similarity without rebuilding vectorization each time.

## Vectorizer Configuration
This POC uses:

```python
TfidfVectorizer(
    analyzer="word",
    ngram_range=(1, 2),
    lowercase=False,
    min_df=1,
    max_df=1.0,
)
```

Design intent:
- `analyzer="word"`: word-level retrieval baseline
- `ngram_range=(1, 2)`: unigrams + useful two-word phrases
- `lowercase=False`: input already lowercased in 03c
- `min_df=1`: keep terms in this small 23-chunk corpus
- `max_df=1.0`: no stop-like term filtering yet

## Artifact Contents
`tfidf_index.joblib` stores a dictionary with:
- `vectorizer`
- `matrix`
- `chunk_ids`
- `metadata`

Row alignment guarantee:
- matrix row `i` corresponds to `chunk_ids[i]` and `metadata[i]`.

## Metadata Preserved Per Chunk
Each stored metadata record keeps:
- `chunk_id`
- `document_id`
- `source_file`
- `source_path`
- `title`
- `chunk_index`
- `text`
- `character_count`
- `normalized_text`
- `normalized_character_count`

Keeping both `text` and `normalized_text` supports future retrieval math plus citation/answer context.

## CLI Usage
Run from repo root with environment bootstrap:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1
python .\pocs\03d_word_tfidf_index\src\build_tfidf_index.py
pytest -v .\pocs\03d_word_tfidf_index\tests
```

Optional path overrides:
- `--input`
- `--index-output`
- `--metadata-output`

## What Success Looks Like
The script prints:
- input path
- output index path
- output metadata path
- chunks read
- TF-IDF matrix shape
- vocabulary size
- sample vocabulary
- `PASS`

## Explicitly Out Of Scope
This POC does not build chatbot behavior, answer generation, customer-facing search, embeddings, BM25, typo search, hybrid retrieval, FastAPI, Docker, AWS, or integrated app code.
