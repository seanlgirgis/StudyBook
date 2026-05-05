from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))

from llm_client import generate_response
from retriever import SimpleRetriever
from service import parse_intent


def test_parse_intent_ignores_small_talk_and_keeps_problem_statement() -> None:
    query = (
        "Hi there. I hope your day is going well. "
        "Our AC is not cooling and airflow is weak in two rooms."
    )
    intent = parse_intent(query)
    assert "ac is not cooling" in intent.intent_text.lower()
    assert any("Hi there" in segment for segment in intent.discarded_segments)


def test_multisentence_query_retrieves_relevant_context() -> None:
    retriever = SimpleRetriever(
        str(BASE_DIR / "data" / "knowledge_base.json"),
        str(BASE_DIR / "config" / "stopwords.json"),
    )
    query = (
        "Hello. We had guests over this weekend and everything was fine. "
        "Now the water heater is leaking and we have inconsistent hot water."
    )
    intent = parse_intent(query)
    docs = retriever.retrieve(intent_text=intent.intent_text, top_k=3)
    combined = " ".join(doc.get("text", "").lower() for doc in docs)
    assert "water heater" in combined
    answer = generate_response(query=query, context_sections="\n\n".join(doc.get("text", "") for doc in docs))
    assert isinstance(answer, str)
    assert answer.strip()
