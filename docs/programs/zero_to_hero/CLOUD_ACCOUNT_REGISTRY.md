# Cloud Account Registry (Non-Secret)

## Purpose
Track cloud/platform account metadata needed for reproducible infra and migration work.

## Security Rule
- Never store passwords, tokens, secret keys, private keys, or credential JSON bodies in this file.
- Store only identifiers, hosts, regions, and ownership metadata.
- Route secrets through encrypted files under `config/secrets/*.enc.json` and local env overlays.

## Provider Registry

| Provider | Account / Workspace ID | Region | Environment | Owner | Status | Last Verified | Notes |
|---|---|---|---|---|---|---|---|
| AWS | `profile:study` | `us-east-1` | `learning` | `<fill>` | `bundle_encrypted_local` | `2026-04-02` | Local `~/.aws` contains `study` and `girgisinv`; encrypted bundle created at `config/secrets/aws.profiles.secrets.enc.json` |
| Azure | `Azure subscription 1` | `<fill>` | `learning` | `seanlgirgis@gmail.com` | `proof_verified_local` | `2026-04-02` | Read-only proof passed via CLI+SDK; subscription `b3811436-61fc-4a3a-a6a9-deb05955076d`, tenant `63843a8e-d51e-47a2-b4d7-eb6973b680dd` |
| GCP | `citi-de-learning` | `us-central1` | `learning` | `seanlgirgis@gmail.com` | `key_present_local` | `2026-04-02` | Real SA key stored in protected local path; env points to secure file |
| Databricks | `workspace:7474660483514142` | `<fill>` | `learning` | `seanlgirgis@gmail.com` | `proof_verified_local` | `2026-04-02` | Read-only proof passed via `/api/2.0/clusters/list`; host + PAT resolved from encrypted secret flow |
| Snowflake | `almakze-gu63101` | `<region/cloud>` | `learning` | `seanlgirgis@gmail.com` | `proof_blocked_backend_connect` | `2026-04-02` | Credentials routed to encrypted secrets; read-only proof resolves SNOWFLAKE_* but connector returned `250001 Could not connect to Snowflake backend` |
| Redshift | `<cluster-or-serverless-workgroup>` | `<region>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | Endpoint host non-secret |
| MongoDB Atlas | `de-learning.zur1dze.mongodb.net` | `atlas` | `learning` | `<fill>` | `provided_needs_test` | `2026-04-02` | URI captured in local secret/env flow |

## Secret Key Mapping (Do Not Put Values Here)

### AWS
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (optional)
- `AWS_DEFAULT_REGION`

### Azure
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_RESOURCE_GROUP`

### GCP
- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GOOGLE_APPLICATION_CREDENTIALS_PATH`

### Databricks
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

### Snowflake
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

### Redshift
- `REDSHIFT_HOST`
- `REDSHIFT_PORT`
- `REDSHIFT_DB`
- `REDSHIFT_USER`
- `REDSHIFT_PASSWORD`

### MongoDB Atlas
- `MONGODB_URI`
- `MONGODB_HOST`
- `MONGODB_USER`
- `MONGODB_PASSWORD`
- `MONGODB_DATABASE`

## Update Checklist
1. Update non-secret identifiers and ownership in this file.
2. Verify matching secret keys exist in encrypted secret files.
3. Record validation result in `docs/programs/zero_to_hero/MIGRATION_BOARD.md` evidence column.

## GCP Key Path Standard
- Expected runtime key path for legacy prompts/notebooks: `D:/Workspace/Technologies/_setup/gcp_key.json`
- Current state (verified 2026-04-02): real key ingested at `D:/Users/shareuser/.studybook/secrets/gcp/citi-de-learning-sa.json`; legacy workspace files still include placeholders and should be cleaned when legacy-path compatibility is no longer required.

## AWS Profile Access Standard
- Preferred runtime profile name: `study` (use `de_learner` only where explicitly required).
- Current state (verified 2026-04-02): local credentials are present under `~/.aws` with profiles `study` and `girgisinv`; encrypted portable bundle exists at `config/secrets/aws.profiles.secrets.enc.json`; use explicit profile names (`study`/`girgisinv`) unless a workload explicitly requires another profile.

## Databricks Access Standard
- Workspace host: `https://dbc-9f35a83d-b4e7.cloud.databricks.com`
- Workspace ID: `7474660483514142`
- Current state (verified 2026-04-02): account email `seanlgirgis@gmail.com`; host + PAT captured in encrypted StudyBook secret flow; proof succeeded (`ok: true`).
- Next action: none for baseline connectivity; keep PAT rotated and update encrypted secret records on change.



## Snowflake Access Standard
- Account identifier: lmakze-gu63101`r
- Current state (verified 2026-04-02): encrypted secret routing complete for SNOWFLAKE_*; proof script present at poc/connection_proofs/python/snowflake_connection_proof.py.
- Latest blocker: Snowflake connector error 250001 backend-connect failure during read-only proof in this environment.

