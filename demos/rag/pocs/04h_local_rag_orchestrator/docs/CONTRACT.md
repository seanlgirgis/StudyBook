# CONTRACT - POC 04h Local RAG Orchestrator

## API Contracts (Planned)

### POST `/ask`
Input:
```json
{
  "query": "string"
}
```

Output:
```json
{
  "original_query": "string",
  "cleaned_intent": "string",
  "service_type": "AC|heating|plumbing|water_heater|appliance|maintenance|unknown",
  "symptoms": ["string"],
  "urgency": "low|normal|urgent|unknown",
  "clarification_needed": true,
  "clarifying_questions": ["string"],
  "confidence": 0.0,
  "retrieved_sections": [
    {
      "id": "string",
      "title": "string",
      "service_type": "string",
      "score": 0,
      "text": "string"
    }
  ],
  "final_answer": "string",
  "draft_answer": "string",
  "provider_used": "local_8bit_intent",
  "final_provider_used": "grok-3|grok_mini|unavailable|none",
  "status": "answered|clarification_needed|final_provider_unavailable|no_context|error",
  "note": "string"
}
```

### GET `/health`
Output:
```json
{
  "ok": true,
  "service": "04h_local_rag_orchestrator"
}
```

## Knowledge Base Record Contract (Planned)
```json
{
  "id": "string",
  "title": "string",
  "service_type": "string",
  "symptoms": ["string"],
  "text": "string"
}
```

## Error Behavior (Planned)
- empty query -> HTTP `400`
- malformed KB -> startup or load error
- local intent provider unavailable -> deterministic intent fallback
- final provider unavailable -> `status = "final_provider_unavailable"` with blank `final_answer`
- no retrieval match -> `status = "no_context"`

## Notes
- Two-stage provider model:
  - Stage A: local 8-bit intent clarification
  - Stage B: Grok final answer generation
- local 8-bit must not be treated as final customer-answer provider.
