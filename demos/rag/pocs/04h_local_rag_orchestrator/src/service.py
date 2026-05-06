"""Service orchestration for POC 04h."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .grok_gateway import call_grok_final_answer, get_grok_config
from .kb_loader import load_kb
from .llm_gateway import call_local_llm
from .retriever import retrieve

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
MAX_CLARIFICATION_ATTEMPTS = 3
SERVICE_TYPES = {
    "AC",
    "heating",
    "plumbing",
    "water_heater",
    "appliance",
    "maintenance",
    "emergency",
    "unknown",
}
CLASSIFICATIONS = {
    "supported",
    "clarification_needed",
    "unsupported",
    "human_escalation_required",
    "multi_intent",
}
URGENCY_VALUES = {"low", "normal", "urgent", "unknown"}

SUPPORTED_CAPABILITIES = [
    "AC repair",
    "AC replacement",
    "heating repair",
    "plumbing leak repair",
    "clogged drains",
    "water heater no hot water",
    "water heater pilot light",
    "maintenance plans",
    "emergency service",
    "appliance repair",
]

UNSUPPORTED_EXAMPLES = [
    "car AC / vehicle air conditioning",
    "vehicle repair",
    "carpet cleaning",
    "vent cleaning / duct cleaning",
    "pest control",
    "roofing",
    "remodeling",
    "electrical panel work",
    "medical/legal/insurance questions",
]

_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def get_intent_prompt(query: str) -> str:
    supported = "; ".join(SUPPORTED_CAPABILITIES)
    unsupported = "; ".join(UNSUPPORTED_EXAMPLES)
    return (
        "You are an intent clarification engine for a home-services intake system. "
        "Return JSON only. "
        "Do not answer the customer. "
        "Do not give repair advice. "
        "Do not write markdown. "
        "Classify each request as supported, clarification_needed, unsupported, or human_escalation_required. "
        "If multiple distinct service requests are present, use classification=multi_intent and provide intents array. "
        f"Supported capabilities: {supported}. "
        f"Unsupported examples: {unsupported}. "
        "If request is unclear or could match multiple service types, set clarification_needed=true "
        "and provide 1-3 concise clarifying questions. "
        "If clear, set clarification_needed=false and clarifying_questions=[]. "
        "For unsupported requests, set classification=unsupported and include unsupported_reason. "
        "Allowed service_type: AC, heating, plumbing, water_heater, appliance, maintenance, emergency, unknown. "
        "Allowed urgency: low, normal, urgent, unknown. "
        "Expected JSON keys: classification, cleaned_intent, service_type, matched_capability, symptoms, urgency, "
        "clarification_needed, clarifying_questions, unsupported_reason, confidence, intents.\n\n"
        f"User query: {query}"
    )


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("empty model response")

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object found")

    depth = 0
    end = -1
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if end < 0:
        raise ValueError("incomplete JSON object")

    candidate = text[start:end]
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload is not an object")
    return parsed


def _classify_single_intent(original_query: str) -> dict[str, Any]:
    cleaned = original_query.strip()
    tokens = _tokenize(cleaned)
    token_set = set(tokens)

    def base(
        classification: str,
        service_type: str,
        capability: str,
        symptoms: list[str],
        urgency: str,
        clarification_needed: bool,
        clarifying_questions: list[str],
        unsupported_reason: str,
        confidence: float,
    ) -> dict[str, Any]:
        return {
            "classification": classification,
            "cleaned_intent": cleaned,
            "service_type": service_type,
            "matched_capability": capability,
            "symptoms": symptoms,
            "urgency": urgency,
            "clarification_needed": clarification_needed,
            "clarifying_questions": clarifying_questions,
            "unsupported_reason": unsupported_reason,
            "confidence": confidence,
        }

    # Unsupported policy
    if {"car", "vehicle", "auto"} & token_set and {"ac", "cooling", "air"} & token_set:
        return base(
            "unsupported",
            "unknown",
            "",
            ["ac", "cooling"],
            "normal",
            False,
            [],
            "Vehicle/car AC requests are outside supported home-services scope.",
            0.95,
        )
    if {"carpet", "carpets"} & token_set and {"clean", "cleaning"} & token_set:
        return base(
            "unsupported",
            "unknown",
            "",
            ["carpet cleaning"],
            "normal",
            False,
            [],
            "Carpet cleaning is outside supported home-services scope.",
            0.95,
        )
    if {"pest", "roof", "roofing", "remodel", "remodeling", "electrical", "panel"} & token_set:
        return base(
            "unsupported",
            "unknown",
            "",
            [],
            "normal",
            False,
            [],
            "This request is outside supported home-services intake scope.",
            0.9,
        )
    if {"medical", "legal", "insurance"} & token_set:
        return base(
            "unsupported",
            "unknown",
            "",
            [],
            "unknown",
            False,
            [],
            "Medical, legal, or insurance advice is outside supported scope.",
            0.95,
        )

    # Supported / Clarification
    if {"sink", "pipe", "leak"} & token_set:
        return base(
            "supported",
            "plumbing",
            "plumbing leak repair",
            sorted(list({"sink", "pipe", "leak"} & token_set)),
            "urgent" if "leak" in token_set else "normal",
            False,
            [],
            "",
            0.9,
        )
    if {"drain", "clog", "clogged", "backup"} & token_set:
        return base(
            "supported",
            "plumbing",
            "clogged drains",
            sorted(list({"drain", "clog", "clogged", "backup"} & token_set)),
            "normal",
            False,
            [],
            "",
            0.88,
        )
    if {"ac", "cooling"} & token_set:
        capability = "AC replacement" if {"replace", "replacement", "new"} & token_set else "AC repair"
        return base(
            "supported",
            "AC",
            capability,
            sorted(list({"ac", "cooling"} & token_set)),
            "urgent" if "no" in token_set and "cooling" in token_set else "normal",
            False,
            [],
            "",
            0.86,
        )
    if {"water", "heater"} & token_set and {"pilot", "light"} & token_set:
        return base(
            "supported",
            "water_heater",
            "water heater pilot light",
            sorted(list({"water", "heater", "pilot", "light"} & token_set)),
            "normal",
            False,
            [],
            "",
            0.87,
        )
    if {"water", "heater"} & token_set and {"hot"} & token_set:
        return base(
            "supported",
            "water_heater",
            "water heater no hot water",
            sorted(list({"water", "heater", "hot"} & token_set)),
            "normal",
            False,
            [],
            "",
            0.87,
        )
    if {"maintenance", "tune", "plan"} & token_set:
        return base(
            "supported",
            "maintenance",
            "maintenance plans",
            sorted(list({"maintenance", "tune", "plan"} & token_set)),
            "low",
            False,
            [],
            "",
            0.84,
        )
    if {"emergency", "urgent", "flood"} & token_set:
        return base(
            "supported",
            "emergency",
            "emergency service",
            sorted(list({"emergency", "urgent", "flood"} & token_set)),
            "urgent",
            False,
            [],
            "",
            0.86,
        )
    if {"appliance", "washer", "dryer", "dishwasher"} & token_set:
        return base(
            "supported",
            "appliance",
            "appliance repair",
            sorted(list({"appliance", "washer", "dryer", "dishwasher"} & token_set)),
            "normal",
            False,
            [],
            "",
            0.83,
        )
    if {"water"} & token_set:
        return base(
            "clarification_needed",
            "unknown",
            "",
            ["water"],
            "normal",
            True,
            [
                "Is this a plumbing leak, a clogged drain, a water heater issue, or another water-related problem?",
                "Where is the issue located (sink, drain, water heater, or somewhere else)?",
            ],
            "",
            0.42,
        )
    return base(
        "clarification_needed",
        "unknown",
        "",
        [],
        "unknown",
        True,
        [
            "Can you share which system is affected (AC, heating, plumbing, water heater, appliance, maintenance, or emergency)?"
        ],
        "",
        0.35,
    )


def _split_intent_segments(text: str) -> list[str]:
    raw_parts = re.split(r"\b(?:and also|also|plus|and)\b|[.!?;]+", text, flags=re.IGNORECASE)
    parts = [p.strip(" ,\t\r\n") for p in raw_parts if p and p.strip(" ,\t\r\n")]
    return parts


def _multi_intent_question(intents: list[dict[str, Any]]) -> str:
    supported = [i for i in intents if i.get("classification") == "supported"]
    unsupported = [i for i in intents if i.get("classification") == "unsupported"]
    if supported and unsupported:
        unsupported_reason = unsupported[0].get("unsupported_reason", "One request is unsupported.")
        supported_label = supported[0].get("matched_capability") or supported[0].get("service_type", "supported service")
        return (
            f"{unsupported_reason} Do you want to continue with the supported issue: {supported_label}?"
        )
    labels: list[str] = []
    for item in supported[:3]:
        label = item.get("matched_capability") or item.get("service_type") or item.get("cleaned_intent", "issue")
        labels.append(str(label))
    if not labels:
        labels = [i.get("cleaned_intent", "issue") for i in intents[:2]]
    if len(labels) == 1:
        return f"I can help with more than one issue. Which should we handle first: {labels[0]}?"
    return f"I can help with more than one issue. Which should we handle first: {labels[0]} or {labels[1]}?"


def _fallback_classification(original_query: str) -> dict[str, Any]:
    cleaned = original_query.strip()
    parts = _split_intent_segments(cleaned)
    if len(parts) >= 2:
        intents = [_classify_single_intent(part) for part in parts]
        meaningful = [
            i
            for i in intents
            if i.get("classification") in {"supported", "unsupported", "clarification_needed"}
            and (i.get("matched_capability") or i.get("unsupported_reason") or i.get("service_type") != "unknown")
        ]
        distinct_supported = {
            (i.get("matched_capability") or i.get("service_type"))
            for i in meaningful
            if i.get("classification") == "supported"
        }
        has_unsupported = any(i.get("classification") == "unsupported" for i in meaningful)
        if len(distinct_supported) >= 2 or (len(distinct_supported) >= 1 and has_unsupported):
            return {
                "classification": "multi_intent",
                "cleaned_intent": cleaned,
                "service_type": "unknown",
                "matched_capability": "",
                "symptoms": sorted(
                    list(
                        {
                            symptom
                            for item in meaningful
                            for symptom in item.get("symptoms", [])
                            if isinstance(symptom, str)
                        }
                    )
                ),
                "urgency": "normal",
                "clarification_needed": True,
                "clarifying_questions": [_multi_intent_question(meaningful)],
                "unsupported_reason": "",
                "confidence": 0.7,
                "intents": [
                    {
                        "classification": item.get("classification", "clarification_needed"),
                        "cleaned_intent": item.get("cleaned_intent", ""),
                        "service_type": item.get("service_type", "unknown"),
                        "matched_capability": item.get("matched_capability", ""),
                        "symptoms": item.get("symptoms", []),
                        "unsupported_reason": item.get("unsupported_reason", ""),
                        "confidence": item.get("confidence", 0.0),
                    }
                    for item in meaningful
                ],
            }

    return _classify_single_intent(original_query)


def _normalize_intent(payload: dict[str, Any], original_query: str) -> dict[str, Any]:
    cleaned = payload.get("cleaned_intent")
    classification = payload.get("classification")
    service_type = payload.get("service_type")
    matched_capability = payload.get("matched_capability")
    symptoms = payload.get("symptoms")
    urgency = payload.get("urgency")
    clarification_needed = payload.get("clarification_needed")
    clarifying_questions = payload.get("clarifying_questions")
    unsupported_reason = payload.get("unsupported_reason")
    confidence = payload.get("confidence")
    intents = payload.get("intents", [])

    if classification not in CLASSIFICATIONS:
        raise ValueError("invalid classification")
    if not isinstance(cleaned, str) or not cleaned.strip():
        raise ValueError("invalid cleaned_intent")
    if service_type not in SERVICE_TYPES:
        raise ValueError("invalid service_type")
    if not isinstance(matched_capability, str):
        raise ValueError("invalid matched_capability")
    if urgency not in URGENCY_VALUES:
        raise ValueError("invalid urgency")
    if not isinstance(symptoms, list) or not all(isinstance(x, str) for x in symptoms):
        raise ValueError("invalid symptoms")
    if not isinstance(clarification_needed, bool):
        raise ValueError("invalid clarification_needed")
    if not isinstance(clarifying_questions, list) or not all(isinstance(x, str) for x in clarifying_questions):
        raise ValueError("invalid clarifying_questions")
    if not isinstance(unsupported_reason, str):
        raise ValueError("invalid unsupported_reason")
    if not isinstance(confidence, (int, float)):
        raise ValueError("invalid confidence")
    if intents is not None and not isinstance(intents, list):
        raise ValueError("invalid intents")

    normalized = {
        "classification": classification,
        "cleaned_intent": cleaned.strip(),
        "service_type": service_type,
        "matched_capability": matched_capability.strip(),
        "symptoms": [x.strip() for x in symptoms if x.strip()],
        "urgency": urgency,
        "clarification_needed": clarification_needed,
        "clarifying_questions": [x.strip() for x in clarifying_questions if x.strip()][:3],
        "unsupported_reason": unsupported_reason.strip(),
        "confidence": max(0.0, min(1.0, float(confidence))),
    }
    if classification == "multi_intent":
        normalized_intents: list[dict[str, Any]] = []
        for item in intents:
            if not isinstance(item, dict):
                continue
            sub_class = item.get("classification", "clarification_needed")
            if sub_class not in {"supported", "unsupported", "clarification_needed"}:
                sub_class = "clarification_needed"
            normalized_intents.append(
                {
                    "classification": sub_class,
                    "cleaned_intent": str(item.get("cleaned_intent", "")).strip(),
                    "service_type": item.get("service_type", "unknown")
                    if item.get("service_type", "unknown") in SERVICE_TYPES
                    else "unknown",
                    "matched_capability": str(item.get("matched_capability", "")).strip(),
                    "symptoms": [
                        str(x).strip()
                        for x in item.get("symptoms", [])
                        if isinstance(x, str) and x.strip()
                    ],
                    "unsupported_reason": str(item.get("unsupported_reason", "")).strip(),
                    "confidence": max(0.0, min(1.0, float(item.get("confidence", 0.0)))),
                }
            )
        normalized["intents"] = normalized_intents
        normalized["clarification_needed"] = True
    return normalized


def clean_intent_with_local_llm(original_query: str) -> dict[str, Any]:
    query = original_query.strip()
    if not query:
        return {
            "classification": "clarification_needed",
            "cleaned_intent": "",
            "service_type": "unknown",
            "matched_capability": "",
            "symptoms": [],
            "urgency": "unknown",
            "clarification_needed": True,
            "clarifying_questions": [
                "Can you describe the issue and tell us whether it is AC, heating, plumbing, water heater, appliance, maintenance, or emergency related?"
            ],
            "unsupported_reason": "",
            "confidence": 0.0,
            "intents": [],
        }

    prompt = get_intent_prompt(query)
    try:
        llm_text = call_local_llm(prompt)
        parsed = _extract_json_object(llm_text)
        return _normalize_intent(parsed, query)
    except Exception:
        return _fallback_classification(query)


def _build_retrieval_query(intent: dict[str, Any], original_query: str) -> str:
    parts: list[str] = [intent.get("cleaned_intent", "") or original_query]
    capability = intent.get("matched_capability", "")
    service_type = intent.get("service_type", "")
    symptoms = intent.get("symptoms", [])
    if capability:
        parts.append(str(capability))
    if service_type and service_type != "unknown":
        parts.append(str(service_type))
    if isinstance(symptoms, list):
        parts.extend([s for s in symptoms if isinstance(s, str)])
    return " ".join([p for p in parts if isinstance(p, str) and p.strip()])


def _build_escalation_package(
    *,
    original_query: str,
    conversation_history: list[str],
    intent: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    known_details = [
        f"cleaned_intent={intent.get('cleaned_intent', '')}",
        f"classification={intent.get('classification', '')}",
        f"service_type={intent.get('service_type', '')}",
        f"symptoms={intent.get('symptoms', [])}",
        f"urgency={intent.get('urgency', '')}",
    ]
    missing_details = [
        "customer_name",
        "phone_number",
        "service_address",
        "preferred_callback_time",
        "short_issue_description",
    ]
    return {
        "original_query": original_query,
        "conversation_history": conversation_history,
        "known_details": known_details,
        "missing_details": missing_details,
        "last_classification": intent.get("classification", "unknown"),
        "last_service_type": intent.get("service_type", "unknown"),
        "last_symptoms": intent.get("symptoms", []),
    }


def answer_query(
    original_query: str,
    clarification_attempt: int = 0,
    conversation_history: list[str] | None = None,
) -> dict[str, Any]:
    history = conversation_history or []
    attempt = max(0, int(clarification_attempt))
    intent = clean_intent_with_local_llm(original_query)

    base = {
        "original_query": original_query,
        "classification": intent["classification"],
        "cleaned_intent": intent["cleaned_intent"],
        "service_type": intent["service_type"],
        "matched_capability": intent["matched_capability"],
        "symptoms": intent["symptoms"],
        "urgency": intent["urgency"],
        "clarification_needed": intent["clarification_needed"],
        "clarifying_questions": intent["clarifying_questions"],
        "unsupported_reason": intent["unsupported_reason"],
        "confidence": intent["confidence"],
        "clarification_attempt": attempt,
        "max_clarification_attempts": MAX_CLARIFICATION_ATTEMPTS,
        "retrieved_sections": [],
        "final_answer": "",
        "draft_answer": "",
        "provider_used": "local_8bit_intent",
        "final_provider_used": "none",
        "status": "error",
        "note": "",
        "intents": intent.get("intents", []),
    }

    if intent["classification"] == "multi_intent":
        base["status"] = "clarification_needed"
        base["clarification_attempt_next"] = attempt + 1
        base["final_provider_used"] = "none"
        base["retrieved_sections"] = []
        base["final_answer"] = ""
        base["note"] = "Multiple intents detected. Please choose which issue to handle first."
        return base

    if intent["classification"] == "unsupported":
        base["status"] = "unsupported_service"
        base["note"] = "Supported services include AC, heating, plumbing, water heater, appliance, maintenance, and emergency intake."
        return base

    if intent["classification"] == "human_escalation_required":
        base["status"] = "human_escalation_required"
        base["reason"] = "Intent classification requested human escalation."
        base["handoff_summary"] = _build_escalation_package(
            original_query=original_query,
            conversation_history=history,
            intent=intent,
            reason=base["reason"],
        )
        base["recommended_next_message"] = (
            "To connect you with a specialist, please share your name, phone number, service address, "
            "preferred callback time, and a short description of the issue."
        )
        return base

    if intent["classification"] == "clarification_needed" or intent["clarification_needed"]:
        if attempt >= MAX_CLARIFICATION_ATTEMPTS:
            base["status"] = "human_escalation_required"
            base["classification"] = "human_escalation_required"
            base["reason"] = "Intent remained unclear after maximum clarification attempts."
            base["handoff_summary"] = _build_escalation_package(
                original_query=original_query,
                conversation_history=history,
                intent=intent,
                reason=base["reason"],
            )
            base["recommended_next_message"] = (
                "To continue, please share your name, phone number, service address, "
                "preferred callback time, and a short description of the issue."
            )
            return base

        base["status"] = "clarification_needed"
        base["final_provider_used"] = "none"
        base["clarification_attempt_next"] = attempt + 1
        base["note"] = "More detail is needed before final answer generation."
        return base

    # Supported path
    records = load_kb(KB_PATH)
    retrieval_query = _build_retrieval_query(intent, original_query)
    retrieved = retrieve(retrieval_query, records, top_k=5)
    base["retrieved_sections"] = [
        {
            "id": item["id"],
            "title": item["title"],
            "service_type": item["service_type"],
            "score": item["score"],
            "text": item["text"],
        }
        for item in retrieved
    ]

    if not base["retrieved_sections"]:
        base["status"] = "no_context"
        base["note"] = "No matching knowledge base sections found."
        return base

    cfg = get_grok_config()
    if not cfg["api_key"]:
        base["status"] = "final_provider_unavailable"
        base["final_provider_used"] = "unavailable"
        base["note"] = "Final provider unavailable; intent and retrieved sections are ready."
        return base

    try:
        final_answer = call_grok_final_answer(
            {
                "original_query": original_query,
                "cleaned_intent": intent["cleaned_intent"],
                "service_type": intent["service_type"],
                "symptoms": intent["symptoms"],
                "urgency": intent["urgency"],
                "retrieved_sections": base["retrieved_sections"],
                "draft_answer": "",
            }
        )
        base["final_answer"] = final_answer
        base["final_provider_used"] = cfg["model"] or "grok-3"
        base["status"] = "answered"
        return base
    except Exception:
        base["status"] = "final_provider_unavailable"
        base["final_provider_used"] = "unavailable"
        base["note"] = "Final provider unavailable; intent and retrieved sections are ready."
        return base
