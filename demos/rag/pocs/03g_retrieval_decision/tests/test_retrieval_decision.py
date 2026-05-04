from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from retrieval_decision import decide_for_query, load_decision_config, load_hybrid_results, run_decision_batch  # noqa: E402
from schemas import HybridQueryInput, RetrievalCandidate, RetrievalDecisionConfig  # noqa: E402


def _candidate(
    *,
    rank: int,
    chunk_id: str,
    score: float,
    source_file: str,
    normalized_text: str,
) -> RetrievalCandidate:
    return RetrievalCandidate(
        rank=rank,
        chunk_id=chunk_id,
        hybrid_score=score,
        word_score=score * 0.7,
        char_score=score * 0.3,
        source_file=source_file,
        title="Synthetic Demo Document",
        section=None,
        text=normalized_text,
        normalized_text=normalized_text,
    )


def _config() -> RetrievalDecisionConfig:
    return RetrievalDecisionConfig(
        strong_match_min_score=0.8,
        weak_match_min_score=0.3,
        no_match_max_score=0.1,
        min_score_gap_for_strong=0.2,
        close_score_delta=0.05,
        max_close_candidates_before_ambiguous=1,
        top_k_window=5,
        source_diversity_ambiguity_threshold=3,
        enable_needs_clarification=True,
        min_query_tokens_for_specificity=3,
        clarification_min_service_areas=2,
    )


def test_strong_match_label_and_reasons() -> None:
    query = HybridQueryInput(
        query="water heater leaking now",
        normalized_query="water heater leaking now",
        results=[
            _candidate(
                rank=1,
                chunk_id="water_heater_policy__chunk_000",
                score=0.92,
                source_file="water_heater_policy.md",
                normalized_text="water heater service and repair guidance",
            ),
            _candidate(
                rank=2,
                chunk_id="faq__chunk_000",
                score=0.50,
                source_file="faq.md",
                normalized_text="general frequently asked questions",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "strong_match"
    assert result.recommended_route == "answer_candidate_path"
    assert "TOP_SCORE_STRONG" in result.reason_codes
    assert "CLEAR_SCORE_GAP" in result.reason_codes
    assert "LOW_CLOSE_CANDIDATE_COUNT" in result.reason_codes


def test_ambiguous_match_label() -> None:
    query = HybridQueryInput(
        query="water heater leaking in garage",
        normalized_query="water heater leaking in garage",
        results=[
            _candidate(
                rank=1,
                chunk_id="water_heater_policy__chunk_000",
                score=0.62,
                source_file="water_heater_policy.md",
                normalized_text="water heater leak policy",
            ),
            _candidate(
                rank=2,
                chunk_id="water_heater_faq__chunk_000",
                score=0.59,
                source_file="faq.md",
                normalized_text="faq on water heater repairs",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "ambiguous_match"
    assert result.precedence_rule_applied == "AMBIGUOUS_MATCH_PRECEDENCE"


def test_weak_match_label() -> None:
    query = HybridQueryInput(
        query="ac condenser noisy",
        normalized_query="ac condenser noisy",
        results=[
            _candidate(
                rank=1,
                chunk_id="hvac_repair_policy__chunk_000",
                score=0.25,
                source_file="hvac_repair_policy.md",
                normalized_text="hvac repair guidance for condenser noise",
            )
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "weak_match"
    assert result.recommended_route == "fallback_path"


def test_no_match_label() -> None:
    query = HybridQueryInput(
        query="help",
        normalized_query="help",
        results=[
            _candidate(
                rank=1,
                chunk_id="company_profile__chunk_000",
                score=0.05,
                source_file="company_profile.md",
                normalized_text="general company profile data",
            )
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "no_match"
    assert result.recommended_route == "no_answer_path"
    assert result.selected_candidate_ids == []


def test_needs_clarification_label() -> None:
    query = HybridQueryInput(
        query="help me",
        normalized_query="help me",
        results=[
            _candidate(
                rank=1,
                chunk_id="hvac_repair_policy__chunk_000",
                score=0.55,
                source_file="hvac_repair_policy.md",
                normalized_text="hvac not cooling service policy",
            ),
            _candidate(
                rank=2,
                chunk_id="water_heater_policy__chunk_000",
                score=0.53,
                source_file="water_heater_policy.md",
                normalized_text="water heater leak policy",
            ),
            _candidate(
                rank=3,
                chunk_id="appliance_policy__chunk_000",
                score=0.51,
                source_file="appliance_repair_policy.md",
                normalized_text="appliance repair policy details",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "needs_clarification"
    assert result.precedence_rule_applied == "CLARIFICATION_BEATS_AMBIGUOUS_OR_WEAK"
    assert "CLARIFICATION_POLICY_TRIGGERED" in result.reason_codes


def test_precedence_ambiguous_but_clarification_wins() -> None:
    query = HybridQueryInput(
        query="issue",
        normalized_query="issue",
        results=[
            _candidate(
                rank=1,
                chunk_id="hvac_repair_policy__chunk_000",
                score=0.61,
                source_file="hvac_repair_policy.md",
                normalized_text="hvac repair details",
            ),
            _candidate(
                rank=2,
                chunk_id="water_heater_policy__chunk_000",
                score=0.59,
                source_file="water_heater_policy.md",
                normalized_text="water heater service details",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "needs_clarification"


def test_precedence_weak_but_clarification_wins() -> None:
    query = HybridQueryInput(
        query="problem",
        normalized_query="problem",
        results=[
            _candidate(
                rank=1,
                chunk_id="general_policy__chunk_000",
                score=0.20,
                source_file="company_profile.md",
                normalized_text="general policy details",
            ),
            _candidate(
                rank=2,
                chunk_id="water_heater_policy__chunk_000",
                score=0.18,
                source_file="water_heater_policy.md",
                normalized_text="water heater service details",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "needs_clarification"


def test_precedence_ambiguous_remains_ambiguous_for_specific_query() -> None:
    query = HybridQueryInput(
        query="water heater leak at base",
        normalized_query="water heater leak at base",
        results=[
            _candidate(
                rank=1,
                chunk_id="water_heater_policy__chunk_000",
                score=0.58,
                source_file="water_heater_policy.md",
                normalized_text="water heater leak diagnostic policy",
            ),
            _candidate(
                rank=2,
                chunk_id="faq__chunk_000",
                score=0.55,
                source_file="faq.md",
                normalized_text="water heater faq and answers",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "ambiguous_match"


def test_precedence_no_match_beats_clarification() -> None:
    query = HybridQueryInput(
        query="help",
        normalized_query="help",
        results=[
            _candidate(
                rank=1,
                chunk_id="hvac_repair_policy__chunk_000",
                score=0.09,
                source_file="hvac_repair_policy.md",
                normalized_text="hvac repair details",
            ),
            _candidate(
                rank=2,
                chunk_id="water_heater_policy__chunk_000",
                score=0.08,
                source_file="water_heater_policy.md",
                normalized_text="water heater details",
            ),
        ],
    )
    result = decide_for_query(query, _config())
    assert result.decision_label == "no_match"


def test_deterministic_repeatability() -> None:
    query = HybridQueryInput(
        query="water heater leaking now",
        normalized_query="water heater leaking now",
        results=[
            _candidate(
                rank=1,
                chunk_id="water_heater_policy__chunk_000",
                score=0.62,
                source_file="water_heater_policy.md",
                normalized_text="water heater service",
            ),
            _candidate(
                rank=2,
                chunk_id="intake_script__chunk_000",
                score=0.60,
                source_file="intake_script.md",
                normalized_text="water heater intake details",
            ),
        ],
    )
    config = _config()
    a = decide_for_query(query, config).model_dump(mode="json")
    b = decide_for_query(query, config).model_dump(mode="json")
    assert a == b


def test_malformed_input_handling() -> None:
    with pytest.raises(ValidationError):
        HybridQueryInput.model_validate({"query": "x", "normalized_query": "x", "results": [{"rank": 1}]})


def test_load_hybrid_results_invalid_payload(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"poc": "03f_hybrid_retrieval"}), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_hybrid_results(path)


def test_load_decision_config_invalid_range(tmp_path: Path) -> None:
    path = tmp_path / "bad_config.json"
    path.write_text(json.dumps({"strong_match_min_score": 1.5}), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_decision_config(path)


def test_run_decision_batch_shape() -> None:
    config = _config()
    batch = run_decision_batch(
        hybrid_batch=load_hybrid_results(
            Path(__file__).resolve().parents[2] / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
        ),
        input_source="pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json",
        config=config,
    )
    assert batch.poc == "03g_retrieval_decision"
    assert len(batch.query_decisions) > 0
