# test_grok_fallback.py
import sys
from pathlib import Path

# Add src folder to Python path so we can import retriever
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from grok_intent_clarification import clarify_intent  # Phase 1 Grok module
from retriever import SimpleRetriever

# Test queries
test_queries = [
    "heatng maintaining plan",
    "plumping issue",
    "AC repar service"
]

# Instantiate local retriever
retriever = SimpleRetriever("data/knowledge_base.json")

print("Phase 1 RAG Interactive Tester with Grok fallback")
print("Type 'exit' to quit.\n")

for query in test_queries:
    # First try local retrieval
    sections = retriever.retrieve(query)
    if sections:
        print("Retrieved using LOCAL retriever:")
    else:
        # Fallback to Grok for query normalization
        normalized = clarify_intent(query)
        sections = retriever.retrieve(normalized)
        print("Retrieved using GROK fallback:")

    print(f"Query: {query}")
    if sections:
        for i, doc in enumerate(sections, 1):
            print(f"{i}. {doc['text']}")
    else:
        print("No context found.")
    print("-"*40)