import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add src folder to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from llm_client import generate_response
from retriever import SimpleRetriever
from service import parse_intent


retriever = SimpleRetriever(
    str(BASE_DIR / "data" / "knowledge_base.json"),
    str(BASE_DIR / "config" / "stopwords.json"),
)

ask_log_path = BASE_DIR / "outputs" / "ask_logs.json"
ask_log_path.parent.mkdir(parents=True, exist_ok=True)

print("Phase 1 RAG Interactive Tester (Multi-Sentence Intent)")
print("Type 'exit' to quit.\n")

while True:
    query = input("Enter query: ").strip()
    if query.lower() == "exit":
        break

    if not query:
        print("Empty query. Skipping retrieval.")
        print("-" * 60)
        continue

    intent = parse_intent(query)
    retrieved_docs = retriever.retrieve(intent_text=intent.intent_text, top_k=3)
    retrieved_sections = [doc.get("text", "") for doc in retrieved_docs if isinstance(doc, dict)]
    answer = generate_response(query=query, context_sections="\n\n".join(retrieved_sections))

    log_entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "intent_text": intent.intent_text,
        "retrieved_sections": retrieved_sections,
        "llm_response": answer,
    }
    with ask_log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"Original Query: {query}")
    print(f"Intent Text: {intent.intent_text}")
    if intent.discarded_segments:
        print(f"Discarded Segments: {intent.discarded_segments}")

    if retrieved_sections:
        print("Retrieved Sections:")
        for idx, section in enumerate(retrieved_sections, start=1):
            print(f"{idx}. {section}")
    else:
        print("No context found.")

    print(f"Answer: {answer}")
    print("-" * 60)
