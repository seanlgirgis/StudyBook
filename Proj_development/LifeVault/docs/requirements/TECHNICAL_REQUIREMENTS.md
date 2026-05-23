# TECHNICAL_REQUIREMENTS.md

- Python-first implementation with explicit config-driven paths.
- SQLite operational schema with migration tracking and validation.
- Migration runner must be idempotent and temp-DB tested first.
- No dependency on local OneDrive hydration for metadata search.
- CLI and future Streamlit control center should share core service logic.
- Logging must avoid secrets and sensitive payload leakage.