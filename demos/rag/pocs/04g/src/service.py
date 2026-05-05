import json
import os
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel


class IntentParseResult(BaseModel):
    original_query: str
    intent_text: str
    service_type: Optional[str] = None
    discarded_segments: list[str] = []


def _deterministic_fallback(query: str) -> IntentParseResult:
    small_talk_phrases = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "please",
        "can you help",
        "how are you",
        "just checking in",
        "just checking",
    }
    service_map = {
        "ac": "AC",
        "air conditioner": "AC",
        "cooling": "AC",
        "water heater": "water heater",
        "pilot light": "water heater",
        "no hot water": "water heater",
        "hot water": "water heater",
        "thermostat": "heating",
        "furnace": "heating",
        "heating": "heating",
        "plumbing": "plumbing",
        "pipe": "plumbing",
        "leak": "plumbing",
        "drain": "plumbing",
    }

    normalized = query.replace("\n", " ").replace("!", ".").replace("?", ".")
    sentences = [part.strip() for part in normalized.split(".") if part.strip()]

    selected_sentence = ""
    discarded_segments: list[str] = []
    non_greeting_sentences: list[str] = []
    for sentence in sentences:
        lowered = sentence.lower().strip(" ,;:-")
        if any(phrase in lowered for phrase in small_talk_phrases):
            discarded_segments.append(sentence.strip())
            continue
        non_greeting_sentences.append(sentence.strip())
        if any(signal in lowered for signal in service_map):
            selected_sentence = sentence.strip()
            break

    if not selected_sentence:
        return IntentParseResult(
            original_query=query,
            intent_text=query,
            service_type=None,
            discarded_segments=non_greeting_sentences,
        )

    selected_lower = selected_sentence.lower()
    detected_service_type: Optional[str] = None
    for key, value in service_map.items():
        if key in selected_lower:
            detected_service_type = value
            break

    return IntentParseResult(
        original_query=query,
        intent_text=selected_sentence,
        service_type=detected_service_type,
        discarded_segments=discarded_segments,
    )


def _extract_first_json_object(text: str) -> str:
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object start found in model response.")
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("No complete JSON object found in model response.")


def parse_intent(query: str) -> IntentParseResult:
    if not query.strip():
        return IntentParseResult(original_query=query, intent_text=query, service_type=None, discarded_segments=[])

    if not os.getenv("OPENAI_API_KEY"):
        return _deterministic_fallback(query)

    prompt = (
        "You are an AI intent extractor for a home services support system.\n\n"
        "Your task is to read a user's input and extract the main service issue.\n\n"
        "Rules:\n"
        "1. Ignore greetings, small talk, pleasantries, and unrelated context.\n"
        "2. Focus only on sentences describing a service problem.\n"
        "3. Identify the type of service:\n"
        "   - AC, plumbing, heating, water heater\n"
        "   - Map specific keywords like 'pilot light' -> 'water heater', 'thermostat' -> 'heating'\n"
        "4. Output only JSON in this exact structure:\n"
        "{\n"
        '  "original_query": "<the full user input>",\n'
        '  "intent_text": "<the core sentence or clause describing the problem>",\n'
        '  "service_type": "<one of AC, plumbing, heating, water heater, or null if unknown>"\n'
        "}\n"
        "Do not write anything else.\n\n"
        f"User input: {query}"
    )

    model_name = os.getenv("INTENT_MODEL", "grok-mini")
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        content = (response.choices[0].message.content or "").strip()
        payload_text = _extract_first_json_object(content)
        payload = json.loads(payload_text)

        result = IntentParseResult(
            original_query=payload.get("original_query") or query,
            intent_text=payload.get("intent_text") or query,
            service_type=payload.get("service_type"),
            discarded_segments=[],
        )
        return result
    except Exception:
        return _deterministic_fallback(query)
