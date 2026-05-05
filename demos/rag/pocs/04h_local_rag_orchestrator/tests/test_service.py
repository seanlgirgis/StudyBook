import src.service as service


def test_intent_prompt_contains_strict_json_instructions() -> None:
    prompt = service.get_intent_prompt("Something is wrong with water.")
    assert "Return JSON only." in prompt
    assert "Do not answer the customer." in prompt


def test_extract_json_object_with_wrapper_text() -> None:
    raw = (
        "Sure, here is the output:\n"
        '{"cleaned_intent":"sink leak","service_type":"plumbing","symptoms":["sink","leak"],'
        '"urgency":"urgent","clarification_needed":false,"clarifying_questions":[],"confidence":0.8}'
        "\nThanks."
    )
    parsed = service._extract_json_object(raw)
    assert parsed["service_type"] == "plumbing"
    assert parsed["clarification_needed"] is False


def test_clean_intent_fallback_marks_ambiguous_query_for_clarification(monkeypatch) -> None:
    def fail_local(_: str, base_url: str = "http://localhost:8002", timeout: int = 180) -> str:
        raise RuntimeError("LLM unavailable")

    monkeypatch.setattr(service, "call_local_llm", fail_local)
    result = service.clean_intent_with_local_llm("Something is wrong with water.")
    assert result["clarification_needed"] is True
    assert result["clarifying_questions"]


def test_answer_query_clarification_needed_path(monkeypatch) -> None:
    def fake_intent(_: str) -> dict:
        return {
            "cleaned_intent": "water issue",
            "service_type": "unknown",
            "symptoms": ["water"],
            "urgency": "normal",
            "clarification_needed": True,
            "clarifying_questions": ["Is this a plumbing leak, drain, or water heater issue?"],
            "confidence": 0.42,
        }

    monkeypatch.setattr(service, "clean_intent_with_local_llm", fake_intent)
    result = service.answer_query("Something is wrong with water.")
    assert result["status"] == "clarification_needed"
    assert result["final_provider_used"] == "none"
    assert result["final_answer"] == ""
    assert result["retrieved_sections"] == []


def test_answer_query_final_provider_unavailable_no_local_final_answer(monkeypatch) -> None:
    def fake_intent(_: str) -> dict:
        return {
            "cleaned_intent": "sink pipe leak",
            "service_type": "plumbing",
            "symptoms": ["sink", "pipe", "leak"],
            "urgency": "urgent",
            "clarification_needed": False,
            "clarifying_questions": [],
            "confidence": 0.9,
        }

    monkeypatch.setattr(service, "clean_intent_with_local_llm", fake_intent)
    monkeypatch.setattr(service, "get_grok_config", lambda: {"api_key": "", "model": "grok-3", "base_url": "https://api.x.ai/v1"})
    called = {"grok": False}

    def fake_grok(_: dict) -> str:
        called["grok"] = True
        return "should not be used"

    monkeypatch.setattr(service, "call_grok_final_answer", fake_grok)

    result = service.answer_query("Water under sink and pipe leaking.")
    assert called["grok"] is False
    assert result["retrieved_sections"]
    assert result["status"] == "final_provider_unavailable"
    assert result["final_provider_used"] == "unavailable"
    assert result["final_answer"] == ""
    assert result["draft_answer"] == ""


def test_answer_query_uses_grok_when_available(monkeypatch) -> None:
    def fake_intent(_: str) -> dict:
        return {
            "cleaned_intent": "ac not cooling",
            "service_type": "AC",
            "symptoms": ["cooling"],
            "urgency": "normal",
            "clarification_needed": False,
            "clarifying_questions": [],
            "confidence": 0.88,
        }

    monkeypatch.setattr(service, "clean_intent_with_local_llm", fake_intent)
    monkeypatch.setattr(service, "get_grok_config", lambda: {"api_key": "x", "model": "grok-3", "base_url": "https://api.x.ai/v1"})
    monkeypatch.setattr(service, "call_grok_final_answer", lambda _: "Final polished KB-grounded answer.")

    result = service.answer_query("My AC is not cooling.")
    assert result["status"] == "answered"
    assert result["final_provider_used"] == "grok-3"
    assert result["final_answer"] == "Final polished KB-grounded answer."

