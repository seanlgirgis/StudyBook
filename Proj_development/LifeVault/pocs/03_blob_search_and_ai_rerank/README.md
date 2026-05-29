# 03 Blob Search And AI Rerank

## What this POC proves
This POC demonstrates a practical LifeVault search pattern:
multiple memory blobs -> one human query -> simple local candidate search -> local AI rerank/elimination -> ranked report.

## How candidate search works
The script tokenizes query + memory text to lowercase words, counts overlap, then adds bonus points for important domain terms:
financial, finance, banking, data, engineer, job, application, february, 2026, recruiter, pyspark, sql, etl.
Top 4 by score become rerank candidates.

## How AI reranking works
The top candidates and query are sent to `POST http://localhost:8002/infer` with a plain-text instruction to return:
- `RANKED_RESULTS`
- `ELIMINATED`

No strict JSON is required for reranking output.

## Why this avoids strict metadata/schema problems
Local retrieval is deterministic and robust; AI only explains/reranks a short candidate list. This reduces dependence on brittle, perfectly-formatted model JSON for primary search recall.

## How to run
From `pocs`:

```powershell
python .\03_blob_search_and_ai_rerank\run_blob_search_rerank.py
```

## Outputs to inspect
- `outputs/local_candidates.json`
- `outputs/ai_rerank_raw.txt`
- `outputs/final_search_report.txt`

## What success looks like
- Local candidate scoring returns sensible top hits.
- `/infer` responds with a readable rerank/elimination note.
- Final report summarizes query, candidates, AI response, and conclusion.
