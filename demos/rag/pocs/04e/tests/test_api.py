from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app import create_app


client = TestClient(create_app())


def test_health_endpoint() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["poc"] == "04e"


def test_query_endpoint_returns_timing_and_results() -> None:
    response = client.post(
        "/v1/query",
        json={
            "query": "Do you offer AC repair?",
            "context_documents": ["services.md"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert "timing" in body
    assert body["timing"]["request_duration_ms"] >= 0.0
    assert body["timing"]["scenario_count"] == body["total"]


def test_answer_endpoint_returns_structured_answer_and_citations() -> None:
    response = client.post(
        "/v1/answer",
        json={
            "query": "Do you offer AC repair?",
            "context_documents": ["services.md"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "answer_ready"
    assert body["route_applied"] == "answer_from_retrieval"
    assert isinstance(body["citations"], list)
    assert body["timing"]["request_duration_ms"] >= 0.0


def test_query_endpoint_rejects_unknown_scenario_id() -> None:
    response = client.post(
        "/v1/query",
        json={
            "query": "Do you offer AC repair?",
            "scenario_ids": ["unknown-scenario"],
        },
    )
    assert response.status_code == 400
    assert "Unknown scenario_id" in response.json()["detail"]


def test_contract_validation_for_missing_query_field() -> None:
    response = client.post("/v1/query", json={"context_documents": []})
    assert response.status_code == 422
