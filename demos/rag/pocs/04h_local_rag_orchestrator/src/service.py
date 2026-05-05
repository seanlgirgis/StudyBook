"""Service orchestration for POC 04h."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .kb_loader import load_kb
from .llm_gateway import call_local_llm
from .retriever import retrieve

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
SERVICE_TYPES = {"AC", "heating", "plumbing", "water_heater", "appliance", "maintenance", "unknown"}
URGENCY_VALUES = {"low", "normal", "urgent", "unknown"}

_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")
_URGENT_TERMS = {"emergency", "urgent", "no", "heat", "cooling", "leak", "flood"}
_SERVICE_KEYWORDS: dict[str, set[str]] = {
    "AC": {"ac", "air", "cool", "cooling", "hvac"},
    "heating": {"heat", "heating", "furnace", "heater"},
    "plumbing": {"plumb", "pipe", "sink", "drain", "leak", "water"},
    "water_heater": {"water", "heater", "pilot", "hot"},
    "appliance": {"appliance", "washer", "dryer", "dishwasher", "fridge"},
    "maintenance": {"maintenance", "tune", "plan", "preventive", "seasonal"},
}


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("empty model response")

    # Fast path for clean JSON output.
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Robust path: find first balanced JSON object.
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


def _infer_service_type(tokens: list[str]) -> str:
    best_type = "unknown"
    best_score = 0
    token_set = set(tokens)
    for label, keywords in _SERVICE_KEYWORDS.items():
        score = len(token_set.intersection(keywords))
        if score > best_score:
            best_type = label
            best_score = score
    return best_type


def _infer_urgency(tokens: list[str]) -> str:
    token_set = set(tokens)
    if "emergency" in token_set or "flood" in token_set:
        return "urgent"
    if "leak" in token_set:
        return "urgent"
    if "no" in token_set and ("heat" in token_set or "cooling" in token_set):
        return "urgent"
    return "normal" if token_set else "unknown"


def _infer_symptoms(tokens: list[str]) -> list[str]:
    symptom_vocab = {
        "leak",
        "pipe",
        "sink",
        "drain",
        "cooling",
        "heat",
        "heater",
        "pilot",
        "water",
        "clogged",
        "flood",
        "emergency",
        "hot",
    }
    return sorted({token for token in tokens if token in symptom_vocab})


def _fallback_intent(original_query: str) -> dict[str, Any]:
    cleaned = original_query.strip()
    tokens = _tokenize(cleaned)
    return {
        "cleaned_intent": cleaned,
        "service_type": _infer_service_type(tokens),
        "symptoms": _infer_symptoms(tokens),
        "urgency": _infer_urgency(tokens),
    }


def _normalize_intent(payload: dict[str, Any], original_query: str) -> dict[str, Any]:
    cleaned = payload.get("cleaned_intent")
    service_type = payload.get("service_type")
    symptoms = payload.get("symptoms")
    urgency = payload.get("urgency")

    if not isinstance(cleaned, str) or not cleaned.strip():
        raise ValueError("invalid cleaned_intent")
    if service_type not in SERVICE_TYPES:
        raise ValueError("invalid service_type")
    if urgency not in URGENCY_VALUES:
        raise ValueError("invalid urgency")
    if not isinstance(symptoms, list) or not all(isinstance(x, str) for x in symptoms):
        raise ValueError("invalid symptoms")

    return {
        "cleaned_intent": cleaned.strip(),
        "service_type": service_type,
        "symptoms": [x.strip() for x in symptoms if x.strip()],
        "urgency": urgency,
    }


def clean_intent_with_local_llm(original_query: str) -> dict[str, Any]:
    query = original_query.strip()
    if not query:
        return {
            "cleaned_intent": "",
            "service_type": "unknown",
            "symptoms": [],
            "urgency": "unknown",
        }

    prompt = (
        "You are an intent normalizer for home-service requests. "
        "Return strict JSON only with keys cleaned_intent, service_type, symptoms, urgency. "
        "Allowed service_type: AC, heating, plumbing, water_heater, appliance, maintenance, unknown. "
        "Allowed urgency: low, normal, urgent, unknown. "
        "Do not include markdown or commentary.\n\n"
        f"User query: {query}"
    )

    try:
        llm_text = call_local_llm(prompt)
        parsed = _extract_json_object(llm_text)
        return _normalize_intent(parsed, query)
    except Exception:
        return _fallback_intent(query)


def answer_query(original_query: str) -> dict[str, Any]:
    intent = clean_intent_with_local_llm(original_query)
    records = load_kb(KB_PATH)
    retrieved = retrieve(intent["cleaned_intent"] or original_query, records, top_k=3)

    slim_sections = [
        {
            "id": item["id"],
            "title": item["title"],
            "service_type": item["service_type"],
            "score": item["score"],
            "text": item["text"],
        }
        for item in retrieved
    ]

    if not slim_sections:
        return {
            "original_query": original_query,
            "cleaned_intent": intent["cleaned_intent"],
            "service_type": intent["service_type"],
            "symptoms": intent["symptoms"],
            "urgency": intent["urgency"],
            "retrieved_sections": [],
            "draft_answer": "I could not find matching knowledge base sections for this request.",
            "provider_used": "local_8bit",
            "status": "no_context",
        }

    context_blob = "\n\n".join(
        [
            f"[{idx+1}] {sec['title']} ({sec['service_type']})\n{sec['text']}"
            for idx, sec in enumerate(slim_sections)
        ]
    )
    prompt = (
        "You are a concise home-services assistant. "
        "Use only these knowledge base sections to answer. "
        "If details are missing, say what is unknown briefly.\n\n"
        f"Knowledge base sections:\n{context_blob}\n\n"
        f"Customer query: {original_query}\n"
        "Answer in one short paragraph."
    )

    try:
        draft_answer = call_local_llm(prompt)
        status = "answered"
    except RuntimeError:
        draft_answer = (
            "Matching knowledge base sections were found, but the local LLM is currently unavailable. "
            "Please retry after the local 8-bit LLM container is running."
        )
        status = "llm_unavailable"

    return {
        "original_query": original_query,
        "cleaned_intent": intent["cleaned_intent"],
        "service_type": intent["service_type"],
        "symptoms": intent["symptoms"],
        "urgency": intent["urgency"],
        "retrieved_sections": slim_sections,
        "draft_answer": draft_answer,
        "provider_used": "local_8bit",
        "status": status,
    }