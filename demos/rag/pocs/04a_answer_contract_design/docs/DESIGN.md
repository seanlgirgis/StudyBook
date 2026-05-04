# 04a Answer Contract Design

## Problem Statement
`03g` can classify retrieval quality and route hints, and `03h` can evaluate whether retrieval/decision behavior is passing known fixtures.  
What is still missing is a strict contract for answer assembly that prevents ungrounded output and handles low-confidence or risky situations safely.

Without this contract, downstream answer generation may:
- overstate facts not supported by retrieved documents
- omit citations
- answer when evidence is weak or ambiguous
- fail to escalate risky scenarios

## Design Goals
- Define stable interfaces between retrieval outputs and answer assembly.
- Enforce citation-backed groundedness for every supported claim.
- Make insufficient evidence an explicit first-class outcome.
- Represent clarification-needed and escalation-required outcomes as structured outputs.
- Keep the design deterministic and auditable before introducing any generation engine.

## Dependencies and Position in Ladder
- Depends on `03f` ranked retrieval candidates as evidence source material.
- Depends on `03g` decision label/route signals to choose answer pathway.
- Depends on `03h` evaluation outputs as quality context for confidence in upstream artifacts.

`04a` does not re-score retrieval and does not change `03g`/`03h` behavior.  
It defines what downstream answer assembly is allowed to do with those outputs.

## System Boundary
Input boundary:
- answer request payload
- retrieval evidence packet (retrieved candidates + decision signals + optional evaluation snapshot)

Output boundary:
- one structured answer-assembly outcome:
  - `answer_ready`
  - `insufficient_evidence`
  - `clarification_needed`
  - `escalation_required`

No live customer text is finalized in this POC.

## Core Data Concepts

### Retrieved Evidence
Raw ranked retrieval outputs (usually top-k) from `03f`, with metadata and scores.  
This is candidate material, not yet approved for answering.

### Selected Evidence
A filtered subset of retrieved evidence that is:
- relevant to the request
- consistent with `03g` decision signal
- adequate for claim support

Selected evidence becomes the only source allowed for citations.

### Answer Draft
Internal structured representation of proposed response content:
- grouped by claims
- each claim mapped to citation ids
- includes confidence/groundedness checks

The draft is not user-final until gates pass.

### Final Answer
User-facing rendered output derived from the approved draft.
Final answer is allowed only when groundedness and safety gates pass.

### Citation Coverage
Coverage score across atomic claims in the draft:
- numerator: claims with at least one valid citation
- denominator: total claims in draft

Target: full coverage for supported factual claims.

### Insufficient Evidence Outcome
Explicit outcome when selected evidence cannot safely support a grounded answer.  
This is not an error; it is expected protective behavior.

## Groundedness Protection Strategy
- Claim-level citation requirement: factual claims must have at least one citation.
- Citation integrity checks: citation must resolve to selected evidence chunk + span/snippet.
- Unsupported claim blocking: unsupported claims cannot flow to final answer.
- Route-aware gating: `03g` route hints constrain answer assembly path.
- Evidence conflict flagging: contradictory selected evidence triggers clarification or escalation path.

## Outcome Branch Logic (Conceptual)
1. `escalation_required` when risk policy is triggered (for example safety/legal/high-impact policy conditions).
2. `clarification_needed` when `03g` indicates unresolved ambiguity or the answer request is underspecified.
3. `insufficient_evidence` when retrieval evidence cannot meet minimum groundedness criteria.
4. `answer_ready` only when evidence sufficiency and citation coverage gates pass.

Branch intent:
- avoid forcing an answer when uncertainty is high
- keep failure modes explicit and machine-readable
- preserve safe fallback behavior

## Clarification Representation
Clarification-required outcomes should include:
- reason codes
- missing information dimensions (for example equipment type, service category, location detail)
- constrained clarification options or prompt templates for next turn

This remains structured metadata in `04a`; no live conversational policy is implemented yet.

## Escalation Representation
Escalation-required outcomes should include:
- escalation reason category (for example safety risk, policy-sensitive, legal-adjacent)
- severity level
- handoff target (dispatch, supervisor, human reviewer)
- do-not-answer flag for disallowed automated responses

## Design Constraints
- synthetic data only
- deterministic interfaces
- no threshold tuning in this step
- no implementation code
- no modifications to completed retrieval POCs

## Handoff to Future POCs
After approval, implementation POCs can use this contract to build:
- schema models
- selection/groundedness validators
- answer-draft builder
- outcome router
- citation rendering helpers

Implementation is gated on this design approval.
