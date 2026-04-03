# Possible Micro-Nuggets To Create (Orchestration)

Current lanes already present:
- `airflow`

## Priority Candidates

1. `prefect`
2. `dagster`
3. `mage`
4. `dbt_cloud_orchestration`
5. `az_data_factory_patterns`
6. `aws_step_functions_for_de`
7. `argo_workflows`
8. `luigi`
9. `temporal_data_pipelines`
10. `control_m_concepts`

## Per-Lane Nugget Menu (Reusable Template)

1. `00_setup/00_prereq_check.py`
2. `00_setup/01_seed_lab.py`
3. `01_dag_basics/01_task_definition.py`
4. `01_dag_basics/02_dependencies.py`
5. `01_dag_basics/03_parameters_and_templates.py`
6. `02_scheduling/01_cron_and_intervals.py`
7. `02_scheduling/02_catchup_backfill.py`
8. `03_retries_alerting/01_retries_backoff.py`
9. `03_retries_alerting/02_sla_timeout.py`
10. `04_data_patterns/01_etl_dag_pattern.py`
11. `04_data_patterns/02_branching_short_circuit.py`
12. `05_state_and_metadata/01_variables_connections.py`
13. `05_state_and_metadata/02_lineage_and_observability.py`
14. `06_deploy_and_ops/01_local_to_prod_promotion.py`
15. `06_deploy_and_ops/02_secrets_and_config.py`
16. `07_interview_drills/01_interview_drills.py`
17. `08_mini_capstone/01_multi_stage_pipeline.py`

## Advanced Orchestration Ideas

- `event_driven_orchestration`: trigger DAGs from messages/events.
- `data_aware_scheduling`: conditional scheduling based on freshness checks.
- `cost_aware_orchestration`: scale-to-zero and runtime budget guardrails.
- `multi_environment_release`: dev/stage/prod pipeline promotion blueprint.
