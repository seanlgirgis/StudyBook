"""FastAPI app for POC 04h local orchestrator."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .service import answer_query


class AskRequest(BaseModel):
    query: str


app = FastAPI(title="POC 04h Local RAG Orchestrator")


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"ok": True, "service": "04h_local_rag_orchestrator"}


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return answer_query(query)
