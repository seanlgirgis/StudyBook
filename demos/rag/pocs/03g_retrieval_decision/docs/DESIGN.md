# 03g Retrieval Decision Design

## Problem Statement
Hybrid retrieval (`03f`) can return ranked candidates even when evidence quality is mixed.

Without a separate decision layer, downstream behavior risks treating weak or ambiguous retrieval as if it were reliable. This can lead to brittle or unsafe responses later in the ladder.

## Why Retrieval Decision Is Separate From Retrieval
Retrieval and retrieval decision solve different problems:
- retrieval answers: "What candidate chunks are most similar?"
- retrieval decision answers: "Are these candidates good enough to trust?"

Keeping them separate provides:
- deterministic quality gates
- simpler debugging (score production vs score interpretation)
- easier threshold tuning without changing retrieval internals
- reusable handoff contract for later POCs

## Scope
`03g` is a deterministic scoring-interpretation layer over existing retrieval output.

In scope:
- inspect `03f` hybrid results
- compute evidence signals
- assign one retrieval decision label
- emit structured reason codes and evidence

Out of scope:
- generating customer answers
- calling LLMs
- choosing final business action
- live clarification interaction
- rebuilding or rerunning `03d`/`03e`/`03f` indexing logic

## Expected Input Surface
Primary input comes from `03f` results for each query, including:
- ranked candidates
- `hybrid_score`
- component scores (`word_score`, `char_score`)
- candidate metadata (`chunk_id`, source metadata)

Config input includes deterministic decision rules such as:
- minimum top-score thresholds
- minimum score-gap thresholds
- maximum count of near-tied candidates
- source-diversity or source-concentration checks

## Decision Labels and Meaning
- `strong_match`: retrieval evidence is clear and stable; one candidate (or one narrow set) dominates with adequate confidence.
- `ambiguous_match`: candidates are plausible but competition is high; no single winner is clearly dominant.
- `weak_match`: some similarity exists but evidence is below quality expectations.
- `no_match`: no candidate clears minimum relevance threshold.
- `needs_clarification`: retrieval is not reliable enough for direct downstream use and should be routed to a clarification path in a later step.

Note:
`needs_clarification` is a decision output label in this POC, not a live prompt action.

## decision_label vs recommended_route
- `decision_label` is the core retrieval-quality classification and must remain in the five-label enum.
- `recommended_route` is a downstream orchestration hint and does not redefine retrieval quality.

Planned route examples:
- `answer_candidate_path`
- `clarification_path`
- `fallback_path`
- `no_answer_path`

## Likely Evidence Signals
Core deterministic signals to inspect:
- top score: `rank_1.hybrid_score`
- score gap: `rank_1.hybrid_score - rank_2.hybrid_score`
- close-candidate count: number of candidates within a configured delta of rank 1
- source diversity: how many distinct documents/titles/sections appear in top-k
- minimum threshold checks: floors for top score and optional floors for component scores

Supporting signals (optional):
- retrieval-source agreement (`word` and `char` both support top candidate vs one-sided support)
- score tail shape across top-k (sharp drop vs flat plateau)

## Deterministic Rule Style (Planned)
Rules are threshold-based and ordered.

Precedence order (explicit):
1. `no_match` wins first:
   - no candidates, or top score below no-match floor.
2. `strong_match` next:
   - strong top score + clear score gap + low close-candidate count.
3. `needs_clarification` next:
   - query is vague or underspecified for multiple plausible service areas, or evidence pattern indicates clarification policy trigger.
4. `ambiguous_match` next:
   - close competing candidates remain, but query specificity is sufficient to keep this as ambiguity rather than clarification-forced.
5. `weak_match` last:
   - low but nonzero evidence that does not satisfy higher-precedence branches.

Why this order matters:
- `no_match` should not be converted into clarification when evidence is too weak.
- `needs_clarification` should beat `ambiguous_match` and `weak_match` when clarification policy is triggered.
- `ambiguous_match` remains available for specific-but-close competitions.

Final threshold values are configuration, not hard-coded constants in design.
Threshold numbers shown in examples are initial placeholders and must be tuned later using retrieval-evaluation fixtures.

## Clarification Trigger Guidance (Planned)
`needs_clarification` is expected to win when one or more clarification triggers are true, such as:
- query ambiguity signal indicates underspecified intent across multiple service families
- high close-candidate cluster across different plausible service areas
- policy flag requires clarification for risk-sensitive or multi-intent phrasing

This does not mean a live clarification question is asked in this POC; it only produces a deterministic label and route hint.

## Edge Cases
- empty candidate list
- only one returned candidate (no rank-2 gap available)
- equal top scores across multiple candidates
- all scores near zero
- missing score fields in malformed input
- inconsistent ranking order in input payload
- overly broad top-k from many unrelated sources
- contradictory modality behavior (high char, very low word, or vice versa)

## Design Boundaries
- deterministic only (no stochastic model behavior)
- retrieval-quality decision only
- no user messaging orchestration
- no integration-lane movement

## Handoff Intent
`03g` should produce a stable and explainable decision artifact that future POCs can consume for:
- clarification UX
- fallback routing
- retrieval evaluation metrics

This POC is the policy bridge between retrieval scores and safe downstream behavior.
