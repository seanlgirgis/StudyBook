# Agent Status

## Current Run (2026-04-20)

**Task ID:** TB-20260420-04  
**Task Type:** FIX  
**Goal:** Fix markdown preview default in running JupyterLab container after restart did not apply.

### Factual Summary

- Loaded required startup/control files per `AGENTS.md` order before edits.
- Diagnosed root cause in live container:
  - JupyterLab version: `4.5.6`.
  - No `/opt/conda/share/jupyter/lab/settings` directory exists in this image.
  - Prior approach mounted to non-existent path, so settings never applied.
- Implemented durable fix:
  - Added user-level JupyterLab settings file at `_infra/jupyter/user-settings/@jupyterlab/docmanager-extension/plugin.jupyterlab-settings`.
  - Updated both compose files to mount `../../_infra/jupyter/user-settings` to `/home/jovyan/.jupyter/lab/user-settings:ro`.
  - Removed unused `_infra/jupyter/lab-settings-overrides.json`.
- Recreated running container (not just restart) so new mounts apply:
  - Removed old `citi_jupyterlab`.
  - Started new `citi_jupyterlab` via compose.
  - Verified mounted settings file exists inside container and contains markdown preview mapping.

### Files Inspected

- `CONTROL_PROTOCOL.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `docs/adr/ADR-INDEX.md`
- `agents/shared/pending_task.md`
- `agents/shared/agent_status.md` (prior run)
- `agents/shared/decision_log.md`
- `_infra/docker/pipeline.yml`
- `_infra/docker/docker-compose.yml`
- `_infra/README.md`
- Live container paths under `/opt/conda/share/jupyter/lab` and `/home/jovyan/.jupyter/lab`

### Files Modified

- `_infra/jupyter/user-settings/@jupyterlab/docmanager-extension/plugin.jupyterlab-settings`
- `_infra/docker/pipeline.yml`
- `_infra/docker/docker-compose.yml`
- `_infra/README.md`
- `_infra/jupyter/lab-settings-overrides.json` (deleted)
- `agents/shared/agent_status.md`
- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`

### Validation

- `docker exec citi_jupyterlab sh -lc "jupyter lab --version"` -> `4.5.6`
- `docker compose -f _infra/docker/pipeline.yml config` (pass; user-settings mount resolves)
- `docker compose -f _infra/docker/docker-compose.yml config` (pass; user-settings mount resolves)
- `docker rm -f citi_jupyterlab && docker compose -f _infra/docker/docker-compose.yml up -d jupyterlab` (pass)
- `docker exec citi_jupyterlab sh -lc "cat /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/docmanager-extension/plugin.jupyterlab-settings"` (pass; expected JSON content)
- Non-blocking environment warnings observed: docker client config access warning and existing `studybook_net` ownership warning.

### Assumptions

- User launches JupyterLab from `citi_jupyterlab` compose service.

### Risks

- Low: already applied to running container; user may need browser hard refresh to clear old UI state.

### Next Step

- In browser: hard refresh JupyterLab and reopen `.md`; if old editor tab remains, close it and reopen the file.

---

**Run completed:** 2026-04-20  
**Status:** DONE
