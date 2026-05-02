# Document Design Notes (Synthetic Demo)

## Why These Docs Are Synthetic
- This project is learning-first and should not process real customer data at this stage.
- Synthetic documents allow realistic testing without privacy, compliance, or legal exposure.

## Why HVAC Is Primary
- HVAC issues are high-frequency and urgency-sensitive in North Texas climates.
- HVAC scenarios provide strong coverage for intake classification, urgency detection, and escalation behavior.
- Secondary services are included to test multi-domain routing and fallback boundaries.

## Why Policies Include Edge Cases
- Edge cases force clearer assistant behavior for unsupported requests and exceptions.
- Pricing, safety, and service-area edge cases are essential for escalation logic testing.
- Edge-case policy text helps evaluate whether retrieval can ground nuanced responses.

## How These Docs Help Test RAG Later
- They provide structured, short factual chunks for retrieval and citation experiments.
- They include conflicting-risk patterns (answer vs fallback vs escalate) for evaluation.
- They map directly to later milestones:
  - answer with citations
  - intake classification
  - lead quality scoring
  - urgency detection
  - outcome logging
