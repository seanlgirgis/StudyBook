# Airflow Docker Stack (StudyBook Tutorial)

This folder provides a fresh, from-scratch Docker setup for Apache Airflow.
It is designed to work even if no prior Airflow Docker stack exists.

## Navigation

- [01_setup_and_config.md](./01_setup_and_config.md)
- [02_deploy_use_and_test.md](./02_deploy_use_and_test.md)

## Quick Start

1. Copy env template:
   `Copy-Item .env.example .env`
2. Initialize Airflow metadata DB and admin user:
   `./scripts/manage.ps1 init`
3. Start services:
   `./scripts/manage.ps1 up`
4. Run smoke tests:
   `./tests/smoke_test.ps1`
5. Open Airflow UI:
   [http://localhost:8088](http://localhost:8088)

Default login from `.env`:
- username: `admin`
- password: `admin`