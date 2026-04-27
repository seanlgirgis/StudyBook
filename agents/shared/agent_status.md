# Agent Status

## Run Metadata

- Date: 2026-04-27
- Task ID: TB-20260427-03
- Task Type: FIX
- Status: DONE

## Factual Summary

- Added `tutorials/06_aws_emr/capstone/fix_emr_serverless_role.ps1` to automate EMR Serverless pass-role fix in the `study` account:
  - validates active account and target S3 bucket,
  - creates (or updates) execution role trust for `emr-serverless.amazonaws.com`,
  - applies inline S3 policy for capstone prefixes (`raw/weblogs`, `processed/weblogs`, `emr-scripts`, `emr-serverless-logs`),
  - sets shell env vars (`AWS_PROFILE`, `AWS_REGION`, `EMR_S3_BUCKET`, `EMR_SERVERLESS_ROLE_ARN`).
- Executed the script successfully for:
  - profile: `study`
  - region: `us-east-1`
  - bucket: `citi-telemetry-data-lake-dev`
- Provisioned role:
  - `arn:aws:iam::357811130281:role/StudyBookEMRServerlessExecutionRole`
- Verified role and policy exist in account.

## Files Created

- `tutorials/06_aws_emr/capstone/fix_emr_serverless_role.ps1`

## Files Modified

- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`
- `agents/shared/agent_status.md`

## Validation Commands

- `powershell -NoProfile -ExecutionPolicy Bypass -File .\\capstone\\fix_emr_serverless_role.ps1 -Profile study -Region us-east-1 -Bucket citi-telemetry-data-lake-dev`
- `aws iam get-role --profile study --role-name StudyBookEMRServerlessExecutionRole --query "Role.Arn" --output text`
- `aws iam get-role-policy --profile study --role-name StudyBookEMRServerlessExecutionRole --policy-name StudyBookEMRServerlessS3Policy --output json`

## Validation Outcomes

- Fix script: PASS.
- Execution role exists with expected same-account ARN.
- Inline S3 policy attached with expected bucket/prefix scope.

## Assumptions

- User intends to run capstone orchestration using `study` as canonical profile and `citi-telemetry-data-lake-dev` as capstone bucket.

## Risks

- Low: IAM role propagation can take short time; if immediate `StartJobRun` retry fails, rerun once after ~30-60 seconds.
- Local agent runtime lacked `boto3`, so end-to-end `orchestrate.py` was not executed from this agent shell (user shell already has working boto3).

## Next Step

- In user shell, set:
  - `$env:EMR_SERVERLESS_ROLE_ARN="arn:aws:iam::357811130281:role/StudyBookEMRServerlessExecutionRole"`
- Then rerun:
  - `python .\\capstone\\orchestrate.py`
