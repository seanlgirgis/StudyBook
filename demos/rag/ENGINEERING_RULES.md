# ServiceCall AI Engineering Rules

## Non-Negotiables

1. Use Pydantic models for all structured inputs, outputs, configs, logs, and AI responses.
2. Use type hints for all public functions.
3. No hardcoded secrets.
4. Every POC must have a README with commands and expected output.
5. Every POC must have at least one test or smoke check.
6. Every answer must include citations or use a fallback.
7. Every risky customer request must produce an escalation decision.
8. Every chat request must produce an outcome event.
9. Every AWS resource must have a cleanup path.
10. Nothing moves to integrated/servicecall-ai/ until it is understood in pocs/.

## Main Principle

Schemas first. Implementation second.
