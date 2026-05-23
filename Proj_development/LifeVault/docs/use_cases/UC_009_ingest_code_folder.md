# UC_009_ingest_code_folder.md

## Goal

Ingest code folders with metadata and context while avoiding secret leakage.

## Safety Boundaries

- No token/secret commit.
- No source mutation by default.

## Dependencies

UC_001 proposal flow, sensitivity detection (UC_002).

## Acceptance Criteria

- Code folder proposal includes language/project signals and secret-risk flags.