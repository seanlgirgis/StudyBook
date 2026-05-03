# 03e Character TF-IDF Typo Search

## Purpose
`03e_char_tfidf_typo_search` builds a typo-tolerant character TF-IDF retrieval index so messy customer typing can still return useful candidate chunks.

## Where This Fits in the RAG Ladder
- `03a` loads documents.
- `03b` chunks documents.
- `03c` normalizes text.
- `03d` builds word TF-IDF for clean-word matching.
- `03e` builds character TF-IDF for typo-tolerant matching.

## What Character TF-IDF Means
Word TF-IDF compares whole words and phrases. Character TF-IDF compares small character windows inside and around words.

Example pieces:
- `repair` -> `rep`, `epa`, `pai`, `air`
- `repaid` -> `rep`, `epa`, `pai`, `aid`

Because these strings share multiple 3-5 character windows, character TF-IDF can still surface related chunks even when spelling is wrong.

## Word TF-IDF vs Character TF-IDF
- Word TF-IDF is strong when wording is clean and close to business terms.
- Character TF-IDF helps when customers misspell words or type noisy variants.

## Why 03e Comes After 03d
Word TF-IDF is the baseline lexical layer. Character TF-IDF is the typo-rescue layer that complements the baseline when input quality drops.

## What 03e Helps With
Examples of noisy queries that can still retrieve useful candidates:
- `ac repiar`
- `watr heater`
- `maintenence plan`
- `air condishner`
- `emergncy service`
- `heater repaid`

## What 03e Does Not Help With
Character TF-IDF does not solve:
- semantic meaning understanding
- word-order reasoning
- truly new out-of-vocabulary business concepts
- dense semantic similarity across documents
- very short vague inputs with little signal

## Example: heater repaid -> heater repair
The strings `repaid` and `repair` overlap on character windows like `rep`, `epa`, and `pai`. That overlap can push repair-related chunks higher than unrelated chunks, even with a typo.

## Candidate Matches, Not Final Intent
03e can surface candidates such as "this query looks close to heater repair content." It must not decide final intent by itself.

## Relationship to Guided Customer Input
Future product UX may include autocomplete, autocorrect-style help, service-intent buttons, and clarification choices. 03e does not implement frontend autocomplete/autocorrect. 03e supports the backend typo-tolerant retrieval layer.

## Inputs
- `..\03c_text_normalization\outputs\normalized_chunks.json`

Required chunk fields:
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

## Outputs
- `outputs\char_tfidf_index.joblib`
- `outputs\char_index_metadata.json`
- `outputs\sample_typo_search_results.json`

`char_tfidf_index.joblib` stores:
- `vectorizer`
- `matrix`
- `chunk_ids`
- `metadata`

Row alignment guarantee:
- matrix row `i` matches `chunk_ids[i]` and `metadata[i]`.

## How to Run
From repo root:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1
python .\pocs\03e_char_tfidf_typo_search\src\build_char_tfidf_index.py
```

Optional CLI overrides:
- `--input`
- `--index-output`
- `--metadata-output`
- `--sample-results-output`

## How to Test
From repo root:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1
pytest -v .\pocs\03e_char_tfidf_typo_search\tests
```

## Design Rules: Standalone, Configurable, Reusable, Chainable
- Standalone script with a thin `main()` wrapper.
- Relative default paths plus argparse overrides.
- Importable core functions for later end-to-end orchestration.
- Pydantic validation at input boundary.

## Boundaries / Non-Goals
This POC does not:
- generate final customer answers
- call an LLM
- use embeddings, FAISS, or BM25
- combine with word TF-IDF yet
- implement hybrid retrieval
- implement frontend autocomplete/autocorrect or clarification UI
- build FastAPI, Docker, AWS, or integrated app code

## Next Step After 03e
Next suggested step is discussion of `03f_hybrid_retrieval`, but do not implement `03f` in this stage.
