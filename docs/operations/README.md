# Operations Guides

Use this folder for repeatable day-to-day runbooks.

## Index

- `docs/operations/system_build_baseline.md` - consolidated machine build baseline (software, cloud access posture, Docker stack, and setup/run methods)

- `docs/operations/env_startup.md` - start environment on any machine
- `docs/operations/secrets_workflow.md` - encrypt/decrypt lifecycle and direct seed-backed secret updates (`scripts/env/set_secret.ps1`)
- `docs/operations/subscription_tracker.md` - subscription renewals and action dates
- `docs/operations/docker_service_dictionary.md` - concise function dictionary for each Docker service in StudyBook infra
- `docs/operations/aws_credentials_workflow.md` - AWS profile login + encrypted credential portability workflow
- `poc/connection_proofs/README.md` - POC connection proof scripts for fast resource reachability checks
- `docs/operations/jobsearch_launchpad.md` - StudyBook launch wrappers for JobSearch with machine-configurable root path
- `docs/operations/jobsearch_direct_mode_playbook.md` - direct-mode jobsearch SOP in StudyBook (applied-before checks, tailored generation, status tracking)
- `docs/operations/jobsite_credentials_workflow.md` - canonical job-site credential save/retrieve workflow using JOBSITE_* keys and skill scripts
- `docs/operations/seed_context_and_decryption_reminder.md` - cross-machine/sandbox DPAPI seed reminder (diagnose with `whoami`, do not re-ask passphrase once seed exists)
- docs/operations/learning_resources.md - curated learning links for LeetCode/graphs and interview prep reminders

