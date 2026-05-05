import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # <--- Added for CORS

from src.llm_client import generate_response
from src.retriever import SimpleRetriever
from src.service import parse_intent

app = FastAPI()

# ---- CORS middleware added ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local testing; can restrict to your website origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "knowledge_base.json"
STOPWORDS_PATH = BASE_DIR / "config" / "stopwords.json"
OUTPUTS_DIR = BASE_DIR / "outputs"
ASK_LOG_PATH = OUTPUTS_DIR / "ask_logs.json"

retriever = SimpleRetriever(str(DATA_PATH), str(STOPWORDS_PATH))


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(content={"ok": True})


@app.get("/ping")
def ping() -> JSONResponse:
    return JSONResponse(content={"ok": True})


@app.get("/ask")
def ask(query: str = Query(..., min_length=1)) -> JSONResponse:
    intent = parse_intent(query)
    intent_text = getattr(intent, "intent_text", query)

    retrieved_docs = retriever.retrieve(intent_text=intent_text, top_k=3)
    retrieved_sections = [doc.get("text", "") for doc in retrieved_docs if isinstance(doc, dict)]
    answer = generate_response(query=query, context_sections="\n\n".join(retrieved_sections))

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "retrieved_sections": retrieved_sections,
        "llm_response": answer,
    }
    with ASK_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return JSONResponse(content={"answer": answer})
