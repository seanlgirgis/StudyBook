# 02c LLM Memory Card With Repair

## What this POC proves
This POC proves a safer end-to-end pattern:
`sample text -> local LLM /infer -> raw response -> Python repair/normalization -> valid memory_card.json`.

## How to run
From `pocs`:

```powershell
python .\02c_llm_memory_card_with_repair\run_memory_card_with_repair.py
```

## What success looks like
- `outputs/memory_card_raw_response.txt` contains the raw LLM answer.
- `outputs/memory_card.json` exists and matches the required schema.
- `outputs/memory_card_report.txt` shows:
  - infer worked
  - elapsed time
  - direct JSON parse result
  - whether repair was needed
  - whether final card is valid

## Why this is safer than trusting raw LLM JSON
LLM output can drift from requested format (extra text, arrays instead of objects, invalid fields). Repair/normalization in Python enforces deterministic schema rules so downstream logic gets consistent, validated data.
