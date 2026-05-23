# UC_004_index_pod_to_database.md

## Goal

Index approved pod metadata into LifeVault DB for search/governance.

## Safety Boundaries

- Temp/test DB-first validation.
- No real DB writes until explicitly authorized workflow.

## Dependencies

Migration runner, schema v0, UC_003.

## Acceptance Criteria

- Indexed records map pod/files/instances/review states.
- Validation checks pass.