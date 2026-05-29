# 01 LLM Ping

## What this POC proves
This POC verifies that Python can reach the local LLM server at `http://localhost:8002`, probe likely API shapes, and get a completion-style response.

## How to run
From `pocs`:

```powershell
python .\01_llm_ping\run_llm_ping.py
```

## Expected outputs
- Console diagnostics showing:
  - URLs tried
  - HTTP status codes
  - response snippets
  - final conclusion
- Saved output file:
  - `01_llm_ping/outputs/llm_ping_response.txt`

## Known limitations
- Endpoint compatibility is inferred from common patterns.
- Model discovery from `/v1/models` may fail on non-OpenAI-compatible servers.
- If the service needs auth headers, this script does not provide them.
