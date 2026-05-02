# Common Failures

## Wrong Path
If the loader points to the wrong docs directory, markdown discovery returns zero files or raises path errors.

## Missing Docs
If `pocs/02_fake_business_docs/data/home_services_demo` is missing or moved, loading fails before validation.

## Empty Markdown Files
Blank files fail Pydantic checks because `text`, `character_count`, and `line_count` must be non-empty/positive.

## Title Extraction Issues
If no markdown heading exists, title falls back to filename-derived title; unexpected filenames can produce odd fallback titles.

## Output Folder Missing
If `outputs/` does not exist, write step must create it; this script handles that automatically.

## Pytest Import Path Issues
If pytest runs from a different working directory, `src` imports can fail unless test path setup adds `pocs/03a_load_documents/src` to `sys.path`.
