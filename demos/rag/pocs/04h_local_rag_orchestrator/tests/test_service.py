import src.service as service


def test_prompt_contains_supported_and_unsupported_policy() -> None:
    prompt = service.get_intent_prompt("Something is wrong with water.")
    assert "Supported capabilities:" in prompt
    assert "car AC / vehicle air conditioning" in prompt
    assert "Return JSON only." in prompt
    assert "Do not answer the customer." in prompt


def test_extract_json_with_wrapper_text() -> None:
    raw = (
        "preface\n"
        '{"classification":"supported","cleaned_intent":"sink leak","service_type":"plumbing",'
        '"matched_capability":"plumbing leak repair","symptoms":["sink","leak"],'
        '"urgency":"urgent","clarification_needed":false,"clarifying_questions":[],'
        '"unsupported_reason":"","confidence":0.82}\n'
        "suffix"
    )
    parsed = service._extract_json_object(raw)
    assert parsed["classification"] == "supported"
    assert parsed["matched_capability"] == "plumbing leak repair"


def test_supported_classification_for_sink_pipe_leak(monkeypatch) -> None:
    monkeypatch.setattr(service, "call_local_llm", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("offline")))
    intent = service.clean_intent_with_local_llm("water under my sink pipe leaking")
    assert intent["classification"] == "supported"
    assert intent["service_type"] == "plumbing"
    assert intent["matched_capability"] == "plumbing leak repair"


def test_unsupported_car_ac() -> None:
    intent = service._fallback_classification("my car AC is not working")
    assert intent["classification"] == "unsupported"
    assert "Vehicle/car AC" in intent["unsupported_reason"]


def test_unsupported_carpet_cleaning() -> None:
    intent = service._fallback_classification("do you clean carpets")
    assert intent["classification"] == "unsupported"
    assert "Carpet cleaning" in intent["unsupported_reason"]


def test_clarification_needed_for_vague_water_query() -> None:
    intent = service._fallback_classification("something is wrong with water")
    assert intent["classification"] == "clarification_needed"
    assert intent["clarification_needed"] is True
    assert any("water heater" in q.lower() for q in intent["clarifying_questions"])


def test_retry_escalation_after_max_attempts(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "clean_intent_with_local_llm",
        lambda _q: {
            "classification": "clarification_needed",
            "cleaned_intent": "water issue",
            "service_type": "unknown",
            "matched_capability": "",
            "symptoms": ["water"],
            "urgency": "normal",
            "clarification_needed": True,
            "clarifying_questions": ["Is this plumbing, drain, or water heater related?"],
            "unsupported_reason": "",
            "confidence": 0.4,
        },
    )
    result = service.answer_query(
        "Something is wrong with water",
        clarification_attempt=3,
        conversation_history=["User: something is wrong", "Agent: clarification request"],
    )
    assert result["status"] == "human_escalation_required"
    assert "handoff_summary" in result
    assert "recommended_next_message" in result


def test_supported_but_no_grok_returns_final_provider_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "clean_intent_with_local_llm",
        lambda _q: {
            "classification": "supported",
            "cleaned_intent": "sink pipe leak",
            "service_type": "plumbing",
            "matched_capability": "plumbing leak repair",
            "symptoms": ["sink", "pipe", "leak"],
            "urgency": "urgent",
            "clarification_needed": False,
            "clarifying_questions": [],
            "unsupported_reason": "",
            "confidence": 0.9,
        },
    )
    monkeypatch.setattr(service, "get_grok_config", lambda: {"api_key": "", "model": "grok-3", "base_url": "https://api.x.ai/v1"})
    result = service.answer_query("water under sink")
    assert result["retrieved_sections"]
    assert result["status"] == "final_provider_unavailable"
    assert result["final_answer"] == ""


def test_grok_not_called_for_unsupported(monkeypatch) -> None:
    called = {"grok": False}

    monkeypatch.setattr(
        service,
        "clean_intent_with_local_llm",
        lambda _q: {
            "classification": "unsupported",
            "cleaned_intent": "car ac not cooling",
            "service_type": "unknown",
            "matched_capability": "",
            "symptoms": ["ac", "cooling"],
            "urgency": "normal",
            "clarification_needed": False,
            "clarifying_questions": [],
            "unsupported_reason": "Vehicle/car AC requests are outside supported home-services scope.",
            "confidence": 0.95,
        },
    )

    def fake_grok(_payload: dict) -> str:
        called["grok"] = True
        return "x"

    monkeypatch.setattr(service, "call_grok_final_answer", fake_grok)
    result = service.answer_query("my car AC is not cooling")
    assert result["status"] == "unsupported_service"
    assert called["grok"] is False


def test_multi_intent_ac_and_plumbing_leak() -> None:
    intent = service._fallback_classification(
        "My AC is not cooling and there is water under my sink."
    )
    assert intent["classification"] == "multi_intent"
    caps = {i.get("matched_capability") for i in intent.get("intents", [])}
    assert "AC repair" in caps
    assert "plumbing leak repair" in caps


def test_multi_intent_water_heater_pilot_and_clogged_drain() -> None:
    intent = service._fallback_classification(
        "My water heater pilot light keeps going out and my kitchen drain is clogged."
    )
    assert intent["classification"] == "multi_intent"
    caps = {i.get("matched_capability") for i in intent.get("intents", [])}
    assert "water heater pilot light" in caps
    assert "clogged drains" in caps


def test_multi_intent_supported_and_unsupported_car_vs_home_ac() -> None:
    intent = service._fallback_classification(
        "My car AC is broken and my home AC is not cooling."
    )
    assert intent["classification"] == "multi_intent"
    classes = {i.get("classification") for i in intent.get("intents", [])}
    assert "supported" in classes
    assert "unsupported" in classes


def test_single_intent_ac_still_supported() -> None:
    intent = service._fallback_classification("My AC is not cooling.")
    assert intent["classification"] == "supported"


def test_single_intent_car_ac_still_unsupported() -> None:
    intent = service._fallback_classification("My car AC is not cooling.")
    assert intent["classification"] == "unsupported"


def test_multi_intent_answer_query_no_retrieval_no_grok(monkeypatch) -> None:
    monkeypatch.setattr(
        service,
        "clean_intent_with_local_llm",
        lambda _q: {
            "classification": "multi_intent",
            "cleaned_intent": "AC not cooling and sink leak",
            "service_type": "unknown",
            "matched_capability": "",
            "symptoms": ["cooling", "sink", "leak"],
            "urgency": "normal",
            "clarification_needed": True,
            "clarifying_questions": ["Which issue should we handle first: AC or plumbing leak?"],
            "unsupported_reason": "",
            "confidence": 0.75,
            "intents": [
                {
                    "classification": "supported",
                    "cleaned_intent": "AC not cooling",
                    "service_type": "AC",
                    "matched_capability": "AC repair",
                    "symptoms": ["cooling"],
                    "unsupported_reason": "",
                    "confidence": 0.82,
                },
                {
                    "classification": "supported",
                    "cleaned_intent": "water under sink leak",
                    "service_type": "plumbing",
                    "matched_capability": "plumbing leak repair",
                    "symptoms": ["sink", "leak"],
                    "unsupported_reason": "",
                    "confidence": 0.84,
                },
            ],
        },
    )
    called = {"grok": False}
    monkeypatch.setattr(service, "call_grok_final_answer", lambda _payload: called.__setitem__("grok", True) or "x")
    result = service.answer_query("My AC is not cooling and there is water under my sink.")
    assert result["status"] == "clarification_needed"
    assert result["classification"] == "multi_intent"
    assert result["retrieved_sections"] == []
    assert result["final_answer"] == ""
    assert called["grok"] is False
