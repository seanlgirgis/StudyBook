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
| AWS | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | For S3/Redshift/Lambda labs |
| Azure | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | For ADF/Synapse/AKS labs |
| GCP | `<fill>` | `<fill>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | For BigQuery/Dataflow/GCS labs |
| Databricks | `<workspace-url-or-id>` | `<region>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | Workspace host only |
| Snowflake | `<account-identifier>` | `<region/cloud>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | Account locator only |
| Redshift | `<cluster-or-serverless-workgroup>` | `<region>` | `<fill>` | `<fill>` | `unknown` | `<fill>` | Endpoint host non-secret |

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

## Update Checklist
1. Update non-secret identifiers and ownership in this file.
2. Verify matching secret keys exist in encrypted secret files.
3. Record validation result in `docs/programs/zero_to_hero/MIGRATION_BOARD.md` evidence column.
