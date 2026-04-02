## Task ID
- TB-20260402-40

## Topic
- Fix de_postgres startup failure caused by legacy Workspace bind mounts and make startup path-agnostic

## Task Type
- FIX

## Files Modified
- _infra/scripts/infra_up.ps1
- _infra/README.md
- agents/shared/agent_status.md
- agents/shared/task_register.md
- agents/shared/decision_log.md

## What Was Done
- Confirmed failing container `de_postgres` was not owned by StudyBook compose.
  - It was created from `D:\Workspace\Basics\Databases\_setup\docker-compose.yml` and had bind mounts to `D:\Workspace\Basics\Databases\_setup\volumes\...`.
- Added preflight cleanup in `infra_up.ps1`:
  - Detect containers for selected group by name.
  - Inspect compose labels.
  - If labels point to `\\Workspace\\`, remove those containers before `docker compose up`.
  - Added escape hatch: `-SkipLegacyCleanup`.
- Updated `_infra/README.md` with path-agnostic/legacy-cleanup notes.

## Validation
- Ran: `pwsh -NoProfile -File D:\StudyBook\_infra\scripts\infra_up.ps1 -Group core`
- Observed automatic removal of legacy containers (`de_postgres`, `de_redis`, `de_cassandra`, `de_neo4j`, `de_influxdb`).
- `core` group started successfully.
- Verified `de_postgres` mounts now:
  - `de_postgres_data:/var/lib/postgresql/data:rw`
  - no `D:\Workspace` bind mounts.
- Verified ownership labels now point to StudyBook:
  - `com.docker.compose.project.config_files = D:\StudyBook\_infra\docker\core.yml`

## Risks
- Existing data from legacy bind-mounted containers is not auto-migrated into new named volumes.
- If a user intentionally runs a separate non-StudyBook stack with same container names, startup will remove those containers unless `-SkipLegacyCleanup` is used.

## Next Step
- Optional: add a one-time migration helper to copy old postgres data directory into the new named volume if historical data continuity is required.
