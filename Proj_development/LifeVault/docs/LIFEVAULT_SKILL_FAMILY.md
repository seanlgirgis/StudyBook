# LIFEVAULT_SKILL_FAMILY.md

## Active Skill Family (`LV_*`)

- `LV_ingest_folder`
- `LV_ingest_onedrive`
- `LV_review_pod`
- `LV_dedupe`
- `LV_extract_text`
- `LV_map_vault`
- `LV_publish_vault`
- `LV_search_memory`
- `LV_ingest_code`
- `LV_security_review`
- `LV_control_center`

## Naming Migration

- Deprecated naming prefix: `ODC_*`
- Future-facing naming prefix: `LV_*`

## Use-Case Alignment

- Skill implementation priorities should follow `docs/use_cases/USE_CASE_INDEX.md`.
- First operator workflow is `LV_ingest_folder v0` (`UC_001` + approval gate + `UC_003`).
- Filename/metadata sensitivity (UC_002) and content sensitivity (UC_011) are separate stages.
- Content extraction/classification requires explicit approval and must follow storage, privacy, and backup policy.
