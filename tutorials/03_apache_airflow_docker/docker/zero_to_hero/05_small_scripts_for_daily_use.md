# 05 - Small Scripts for Daily Use

Back: [00_START_HERE.md](./00_START_HERE.md)

This folder includes two beginner helper scripts.

## Script A: `scripts/deploy_groups.ps1`

Purpose: deploy using grouped compose files.

Commands:
- `./scripts/deploy_groups.ps1 init`
- `./scripts/deploy_groups.ps1 up`
- `./scripts/deploy_groups.ps1 down`
- `./scripts/deploy_groups.ps1 ps`
- `./scripts/deploy_groups.ps1 destroy` (safe prompt before deleting volumes/data)
- `./scripts/deploy_groups.ps1 destroy -Force` (no prompt; automation use)

## Script B: `scripts/newbie_dag.ps1`

Purpose: common DAG actions without remembering long docker commands.

Commands:
- `./scripts/newbie_dag.ps1 list`
- `./scripts/newbie_dag.ps1 unpause`
- `./scripts/newbie_dag.ps1 trigger`
- `./scripts/newbie_dag.ps1 state`

Default DAG used by this helper:
- `studybook_docker_hello`
