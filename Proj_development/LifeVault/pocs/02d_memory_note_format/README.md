# 02d Memory Note Format

## What this POC proves
This POC shows an alternative to strict JSON prompting:
`sample text -> local LLM label-based note -> Python parser/normalizer -> saved memory note files`.

## Why label-based output may work better than strict JSON
For local LLMs that sometimes truncate or drift, a short label format is often easier to produce consistently. Python can then normalize sections into a stable structure without requiring perfectly valid model JSON.

## How to run
From `pocs`:

```powershell
python .\02d_memory_note_format\run_memory_note.py
```

## Outputs to inspect
- `outputs/memory_note_raw.txt` (raw model answer)
- `outputs/memory_note_clean.txt` (cleaned label-based note)
- `outputs/memory_note.json` (Python-structured version)
- `outputs/memory_note_report.txt` (run status and parsing summary)

## What success looks like
- `/infer` call succeeds.
- Label sections are detected.
- Final note is non-empty.
- JSON output is generated from parsed labels.
