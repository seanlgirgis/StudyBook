"""Deterministic keyword retriever for POC 04h."""

from __future__ import annotations

import re
from typing import Any

_TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_PATTERN.findall(text.lower())


def retrieve(query: str, records: list[dict[str, Any]], top_k: int = 3) -> list[dict[str, Any]]:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scored: list[dict[str, Any]] = []
    for record in records:
        title_tokens = set(_tokenize(str(record.get("title", ""))))
        service_tokens = set(_tokenize(str(record.get("service_type", ""))))
        symptom_tokens = set(_tokenize(" ".join(record.get("symptoms", []))))
        text_tokens = set(_tokenize(str(record.get("text", ""))))

        score = 0
        for token in query_tokens:
            if token in title_tokens:
                score += 5
            if token in service_tokens:
                score += 4
            if token in symptom_tokens:
                score += 3
            if token in text_tokens:
                score += 1

        if score > 0:
            item = dict(record)
            item["score"] = score
            scored.append(item)

    scored.sort(key=lambda x: (-int(x["score"]), str(x.get("id", ""))))
    return scored[:top_k]