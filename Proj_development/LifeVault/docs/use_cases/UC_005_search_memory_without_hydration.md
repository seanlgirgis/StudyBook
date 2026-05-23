# UC_005_search_memory_without_hydration.md

## Goal

Search LifeVault metadata map without hydrating full OneDrive content locally.

## Safety Boundaries

- Metadata query only.
- No remote copy/sync operations.

## Dependencies

UC_004 indexed metadata, query interface.

## Acceptance Criteria

- Query returns relevant file/pod/source pointers and statuses.
- No file hydration required.