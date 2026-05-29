# 02 LLM Memory Card

## What this POC proves
This POC verifies Python can send a text note to the local LLM and request a strict JSON memory-card structure for downstream indexing/retrieval.

## How to run
From `pocs`:

```powershell
python .\02_llm_memory_card\run_memory_card.py
```

## Expected outputs
- Raw model output:
  - `02_llm_memory_card/outputs/memory_card_raw_response.txt`
- If valid JSON:
  - `02_llm_memory_card/outputs/memory_card.json`
- If invalid JSON:
  - `02_llm_memory_card/outputs/memory_card_parse_error.txt`

## Known limitations
- Uses a best-effort endpoint strategy (`/v1/chat/completions`, then `/v1/completions`).
- Assumes no auth is required.
- A model that ignores formatting instructions may still return non-JSON text.
