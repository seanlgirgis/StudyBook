# Command Allowlist

## Local Dev
- `python --version`
- `pip list`
- `docker --version`
- `docker compose up -d`
- `docker compose down`

## SQL / Data
- `python *.py`
- `pytest`
- local SQL client commands for lab setup/teardown

## Cloud (AWS)
- `aws sts get-caller-identity`
- `aws s3 ls`
- `aws logs describe-log-groups`

## Safety
- Prefer read-only cloud commands unless a lab explicitly requires write actions.
