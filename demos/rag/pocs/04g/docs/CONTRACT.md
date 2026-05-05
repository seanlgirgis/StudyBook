# CONTRACT - POC 04g Local LLM Container API

## API Surface
POC 04g validates two endpoints exposed by the standalone containerized FastAPI service.

## Endpoint: Health
Method:
- `GET /health`

Success response:
```json
{"ok": true}
```

Semantics:
- verifies API process is reachable and running
- does not verify answer quality

## Endpoint: Inference
Method:
- `POST /infer`

Request body schema:
```json
{"query": "string"}
```

Response body schema:
```json
{"answer": "string"}
```

Semantics:
- accepts a user query string
- generates a short model answer from mounted local model files

## Error Behavior
`POST /infer`:
- empty or whitespace-only query -> HTTP `400`
  - detail: `"Query cannot be empty"`
- internal model/tokenization/generation failure -> HTTP `500`
  - detail contains exception text

## Notes
- This contract describes current observed behavior only.
- This POC is a standalone local LLM container proof, not full RAG.