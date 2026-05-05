# interactive_rag_test.py
from src.retriever import SimpleRetriever
from src.service import parse_intent
from src.llm_client import generate_response
import json

# Load the knowledge base
retriever = SimpleRetriever("data/knowledge_base.json")

print("=== Phase 1 RAG Interactive Tester ===")
print("Type 'exit' to quit.\n")

while True:
    query = input("Enter your query: ").strip()
    if query.lower() == "exit":
        break
    if not query:
        continue

    # Run deterministic parser
    intent = parse_intent(query)
    intent_text = getattr(intent, "intent_text", query)

    # Retrieve relevant sections
    retrieved_docs = retriever.retrieve(intent_text)
    retrieved_sections = [doc["text"] for doc in retrieved_docs]

    # Generate answer (simulated or real LLM)
    answer = generate_response(query, "\n\n".join(retrieved_sections))

    # Show results
    print("\n--- Results ---")
    print(f"Query: {query}")
    print("Retrieved Sections:")
    if retrieved_sections:
        for idx, section in enumerate(retrieved_sections, 1):
            print(f"{idx}. {section}")
    else:
        print("No context found.")
    print(f"Answer: {answer}")
    print("----------------\n")