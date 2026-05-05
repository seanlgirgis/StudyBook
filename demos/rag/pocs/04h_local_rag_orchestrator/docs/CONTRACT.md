# CONTRACT - POC 04h Local RAG Orchestrator

## API
### GET `/health`
Response:
```json
{"ok": true}
```

### POST `/ask`
Request body:
```json
{"query": "string"}
```

Response body shape:
```json
{
  "original_query": "string",
  "cleaned_intent": "string",
  "service_type": "AC|heating|plumbing|water_heater|appliance|maintenance|unknown",
  "symptoms": ["string"],
  "urgency": "low|normal|urgent|unknown",
  "retrieved_sections": [
    {
      "id": "string",
      "title": "string",
      "service_type": "string",
      "score": 0,
      "text": "string"
    }
  ],
  "draft_answer": "string",
  "provider_used": "local_8bit",
  "status": "answered|no_context|llm_unavailable"
}
```

## Internal Module Contracts
### `load_kb(path: str | Path) -> list[dict]`
Required record fields:
- `id`
- `title`
- `service_type`
- `symptoms`
- `text`

Failure behavior:
- malformed structure/record -> `ValueError`

### `retrieve(query: str, records: list[dict], top_k: int = 3) -> list[dict]`
- deterministic token-based scoring
- stronger weight for `title`, `service_type`, `symptoms`
- returns only records with score > 0
- each result includes `score`

### `call_local_llm(prompt: str, base_url: str = "http://localhost:8002", timeout: int = 180) -> str`
- POST `{base_url}/infer` with `{"query": prompt}`
- returns `response["answer"]`
- LLM/network/shape failure -> `RuntimeError`

### `clean_intent_with_local_llm(original_query: str) -> dict`
Expected JSON output from LLM:
```json
{
  "cleaned_intent": "...",
  "service_type": "AC|heating|plumbing|water_heater|appliance|maintenance|unknown",
  "symptoms": ["..."],
  "urgency": "low|normal|urgent|unknown"
}
```
If unavailable or parse failure:
- deterministic fallback output

### `answer_query(original_query: str) -> dict`
Flow:
- clean intent
- load KB
- retrieve top KB sections
- assemble grounded prompt
- call local LLM for draft answer
- fallback if LLM unavailable

Status values:
- `answered`
- `no_context`
- `llm_unavailable`