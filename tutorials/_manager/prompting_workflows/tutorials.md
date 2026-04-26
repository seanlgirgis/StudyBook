# Prompting Workflow - Tutorial Code Generation
Last updated: 2026-04-26

## Current Rule

Prefer `prompt_READY_TO_PASTE.md` when present.

- If `prompt_READY_TO_PASTE.md` exists: use it directly in ChatGPT.
- If only `prompt.md` exists: convert/write READY_TO_PASTE first, then generate code.

## Generation Loop (One Topic At A Time)

1. Open the topic folder and confirm status in `_manager/ROADMAP.md`.
2. Paste full `prompt_READY_TO_PASTE.md` into ChatGPT.
3. Generate files sequentially (`file 01`, `file 02`, ... capstone/tests).
4. Save files immediately to the exact topic folder.
5. Run topic tests/scripts locally.
6. Update manager docs with:
   - artifact presence,
   - status class,
   - verification source (`independently verified` vs `user-reported working`).

## Status Labeling Rule

Never write just "working" without verification source.

- `independently verified`: this session contains run output/log evidence.
- `user-reported working`: owner confirmed, not re-run this session.

## PySpark Topic 02 Rule

- `02_pyspark` is canonical local `local[*]` tutorial.
- `02_PySpark_Docker` is a separate Docker/Spark-cluster variant.
- Do not merge/rename/archive either track unless explicitly requested.

## Minimal Validation Commands

```powershell
cd D:\Workarea\StudyBook\tutorials
pytest 10_python_logging\capstone\test_pipeline_logger.py -v
pytest 12_parquet\test_capstone.py -v
pytest 13_python_concurrency\test_capstone.py -v
pytest 14_encryption\capstone\test_encryption.py -v
```

Use topic-specific AWS commands for cloud tutorials after environment bootstrap.
