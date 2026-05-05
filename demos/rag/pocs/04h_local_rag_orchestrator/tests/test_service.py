import src.service as service


def test_clean_intent_fallback_without_llm(monkeypatch) -> None:
    def fake_call_local_llm(prompt: str, base_url: str = "http://localhost:8002", timeout: int = 180) -> str:
        raise RuntimeError("LLM unavailable")

    monkeypatch.setattr(service, "call_local_llm", fake_call_local_llm)

    result = service.clean_intent_with_local_llm(
        "Emergency: no cooling and leak near pipe"
    )
    assert result["cleaned_intent"]
    assert result["urgency"] in {"urgent", "normal", "unknown"}


def test_answer_query_with_monkeypatched_llm(monkeypatch) -> None:
    def fake_call_local_llm(prompt: str, base_url: str = "http://localhost:8002", timeout: int = 180) -> str:
        if "Return strict JSON only" in prompt:
            return (
                '{"cleaned_intent":"water leaking under sink","service_type":"plumbing",'
                '"symptoms":["water","sink","leak"],"urgency":"urgent"}'
            )
        return "A plumber can inspect and repair the leaking sink pipe promptly."

    monkeypatch.setattr(service, "call_local_llm", fake_call_local_llm)

    result = service.answer_query("There is water under my sink and a pipe leak")
    assert result["status"] == "answered"
    assert result["provider_used"] == "local_8bit"
    assert result["retrieved_sections"]
    assert "plumb" in result["service_type"].lower()


def test_answer_query_llm_unavailable_for_draft(monkeypatch) -> None:
    def fake_call_local_llm(prompt: str, base_url: str = "http://localhost:8002", timeout: int = 180) -> str:
        if "Return strict JSON only" in prompt:
            return (
                '{"cleaned_intent":"water leaking under sink","service_type":"plumbing",'
                '"symptoms":["water","sink","leak"],"urgency":"urgent"}'
            )
        raise RuntimeError("draft unavailable")

    monkeypatch.setattr(service, "call_local_llm", fake_call_local_llm)
    result = service.answer_query("Sink leak and water under cabinet")

    assert result["status"] == "llm_unavailable"
    assert "local LLM is currently unavailable" in result["draft_answer"]