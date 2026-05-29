# 01b LLM API Discovery

## What this POC proves
This POC probes the local LLM container at `http://localhost:8002` to discover its real HTTP API shape by testing common GET and POST routes and payload formats.

## How to run
From `pocs`:

```powershell
python .\01b_llm_api_discovery\discover_llm_api.py
```

## Output files to inspect
- `01b_llm_api_discovery/outputs/api_discovery_results.json`
  - Full request-by-request diagnostics.
- `01b_llm_api_discovery/outputs/api_discovery_summary.txt`
  - Quick readable summary, including non-404 and 2xx responses.
- `01b_llm_api_discovery/outputs/openapi.json`
  - Saved only if `/openapi.json` returns 2xx.

## How to identify the correct endpoint
1. Find POST routes with `status_code` in 2xx.
2. Check response body previews for generated text or expected inference fields.
3. If `openapi.json` exists, look for inference-like paths and required payload schema.
4. Use the discovered route + payload shape to update `01_llm_ping` and `02_llm_memory_card`.

## Known limitations
- This probe tests a finite set of common routes and payloads.
- Some APIs may require auth headers or model identifiers not included here.
- Success heuristic is primarily based on HTTP 2xx status.
