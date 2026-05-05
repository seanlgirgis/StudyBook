# test_retriever.py
from src.retriever import SimpleRetriever
from src.service import parse_intent
from src.llm_client import generate_response
import json

# Load retriever
retriever = SimpleRetriever(
    "data/knowledge_base.json",
    "config/stopwords.json"  # load stopwords from config
)

# Example queries including exact, partial, and miswritten
queries = [
    "AC repair",
    "AC Repair Service",
    "A/C repair",
    "Heating maintenance plan",
    "Water Heater Repair",
    "Plumbing issue",
    "heatng maintaining plan",
    "plumping issue"
]

for q in queries:
    intent = parse_intent(q)
    retrieved_docs = retriever.retrieve(intent.intent_text)
    context_text = "\n\n".join([doc["text"] for doc in retrieved_docs])
    answer = generate_response(q, context_text)
    print(f"Query: {q}")
    print(f"Retrieved Sections: {json.dumps([doc['text'] for doc in retrieved_docs], indent=2)}")
    print(f"Answer: {answer}")
    print("-" * 80)