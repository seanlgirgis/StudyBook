# interactive_loopback.py
import json
import time
from pathlib import Path
from grok_intent_clarification import clarify_intent
from retriever import SimpleRetriever
from utils import load_word_replacements, apply_word_replacements

# Load local retriever
retriever = SimpleRetriever("data/knowledge_base.json")

# Load word replacements
replacements = load_word_replacements("config/word_replacements.json")

# Interactive loop
print("Phase 1 RAG Interactive Tester with Loopback")
print("Type 'exit' to quit.\n")

while True:
    query = input("Enter query: ").strip()
    if query.lower() == "exit":
        break

    if not query:
        print("Empty query. Skipping retrieval.")
        print("-"*60)
        continue

    # Apply word replacements first
    preprocessed = apply_word_replacements(query, replacements)

    # Local retrieval
    sections = retriever.retrieve(preprocessed)
    source = "LOCAL"

    if not sections:
        # Grok fallback with simple retry
        normalized = None
        retries = 3
        for attempt in range(retries):
            try:
                normalized = clarify_intent(preprocessed)
                break
            except Exception as e:
                print(f"[Attempt {attempt+1}] Grok call failed: {e}")
                time.sleep(1)
        if not normalized:
            normalized = preprocessed
            source = "NO_MATCH"
        else:
            sections = retriever.retrieve(normalized)
            source = "GROK"

        # Log failed queries
        failed_log_path = Path("outputs/failed_queries.jsonl")
        failed_log_path.parent.mkdir(parents=True, exist_ok=True)
        with failed_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "original_query": query,
                "preprocessed": preprocessed,
                "normalized": normalized,
                "source": source
            }) + "\n")

    print(f"Query: {query} | Source: {source}")
    if sections:
        for i, doc in enumerate(sections, 1):
            print(f"{i}. {doc['text']}")
    else:
        print("No context found.")
    print("-"*60)