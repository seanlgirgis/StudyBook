"""Helpers for deterministic fixture-to-upstream alignment in 03h."""

from __future__ import annotations

from schemas import (
    AlignedCaseResult,
    LabeledRetrievalFixture,
    UpstreamDecisionOutput,
    UpstreamDecisionRecord,
    UpstreamRetrievalOutput,
    UpstreamRetrievalQueryRecord,
)


def build_query_lookup_key(*, normalized_query: str | None, query: str) -> str:
    """Build deterministic key: normalized_query first, then query fallback."""

    if normalized_query is not None and normalized_query.strip():
        return normalized_query.strip().lower()
    return query.strip().lower()


def _build_unique_lookup(
    *,
    records: list[UpstreamRetrievalQueryRecord] | list[UpstreamDecisionRecord],
    source_label: str,
) -> dict[str, UpstreamRetrievalQueryRecord | UpstreamDecisionRecord]:
    lookup: dict[str, UpstreamRetrievalQueryRecord | UpstreamDecisionRecord] = {}
    duplicates: set[str] = set()

    for record in records:
        key = build_query_lookup_key(normalized_query=record.normalized_query, query=record.query)
        if key in lookup:
            duplicates.add(key)
            continue
        lookup[key] = record

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise ValueError(f"duplicate upstream query key(s) in {source_label}: {duplicate_list}")

    return lookup


def align_fixture_cases_to_upstream(
    fixture: LabeledRetrievalFixture,
    retrieval_output: UpstreamRetrievalOutput,
    decision_output: UpstreamDecisionOutput,
) -> list[AlignedCaseResult]:
    """Align fixture cases to 03f/03g query records using deterministic query keys."""

    retrieval_lookup = _build_unique_lookup(records=retrieval_output.queries, source_label="03f")
    decision_lookup = _build_unique_lookup(records=decision_output.query_decisions, source_label="03g")

    aligned: list[AlignedCaseResult] = []
    for case in fixture.cases:
        key = build_query_lookup_key(normalized_query=case.normalized_query, query=case.query)
        retrieval_match = retrieval_lookup.get(key)
        decision_match = decision_lookup.get(key)

        matched_03f = retrieval_match is not None
        matched_03g = decision_match is not None

        if matched_03f and matched_03g:
            status = "matched"
        elif not matched_03f and not matched_03g:
            status = "missing_both"
        elif not matched_03f:
            status = "missing_03f"
        else:
            status = "missing_03g"

        aligned.append(
            AlignedCaseResult(
                case_id=case.case_id,
                fixture_case=case,
                retrieval_record=retrieval_match if isinstance(retrieval_match, UpstreamRetrievalQueryRecord) else None,
                decision_record=decision_match if isinstance(decision_match, UpstreamDecisionRecord) else None,
                matched_03f=matched_03f,
                matched_03g=matched_03g,
                alignment_status=status,
            )
        )

    return aligned
