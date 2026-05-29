# 02b Memory Card Repair

## What this POC proves
This POC shows that Python can repair and normalize imperfect LLM output into a strict LifeVault memory-card shape, even when the model returns a list instead of a single object.

## How to run
From `pocs`:

```powershell
python .\02b_memory_card_repair\repair_memory_card.py
```

## What success looks like
- Script reads `sample_bad_llm_output.txt`.
- Script normalizes output to the exact target schema.
- Script writes:
  - `02b_memory_card_repair/outputs/repaired_memory_card.json`
  - `02b_memory_card_repair/outputs/repair_report.txt`
- Tags are capped at 6 and confidence is constrained to `low|medium|high`.

## Why LLM output is suggested data, not trusted data
LLM output may be structurally wrong (array vs object), partially malformed, or violate constraints (extra tags, invalid enum values). Treating model output as suggested data and enforcing deterministic validation/repair in Python prevents downstream failures and keeps data quality predictable.
