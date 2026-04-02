# Docker Service Dictionary

Purpose: quick function reference for every service in the StudyBook Docker stack.

Source of truth for runtime definition:
- `_infra/docker/docker-compose.yml`

## Core Data Services

### Postgres (`de_postgres`)
Primary relational database for project datasets, seed data, and SQL-focused learning tasks. It is the default backend for telemetry tables and other tabular exercises where transactional consistency matters.

### Redis (`de_redis`)
In-memory key-value store used for caching, fast lookups, and simple queue/state patterns. It is useful when notebook examples need low-latency reads or ephemeral coordination state.

### Cassandra (`de_cassandra`)
Wide-column NoSQL database for high-write and partitioned time-series/event-style workloads. It supports learning scenarios around denormalized modeling and scale-out query patterns.

### Neo4j (`de_neo4j`)
Graph database used for relationship-heavy data problems such as lineage, dependency analysis, and network modeling. It is helpful for traversals and pattern matching that are cumbersome in relational tables.

### InfluxDB (`de_influxdb`)
Time-series database for metrics and observability-style data. It supports high-ingest timestamped measurements and aggregate queries over time windows.

## Streaming Services

### Zookeeper (`citi_zookeeper`)
Coordination layer for the Kafka broker in this stack. It maintains broker metadata and synchronization primitives required by this Kafka deployment mode.

### Kafka (`citi_kafka`)
Distributed event streaming platform for producer/consumer pipelines and durable topic-based messaging. It is the backbone for streaming labs and end-to-end data flow exercises.

### Kafka UI (`citi_kafka_ui`)
Web interface for inspecting Kafka clusters, topics, consumer groups, and messages. It is used for quick operational visibility without running CLI commands for every check.

## Pipeline and Orchestration Services

### Spark Master (`citi_spark`)
Cluster coordinator for distributed Spark workloads in the local environment. It schedules jobs and provides the Spark master web UI for execution visibility.

### Spark Worker (`citi_spark_worker`)
Execution node that runs Spark tasks assigned by the Spark master. It provides compute resources for notebook and pipeline jobs executed through the Spark cluster.

### Airflow (`citi_airflow`)
Workflow orchestration service for DAG-based scheduling and dependency management. It is used to model and run repeatable data pipelines with retry, logging, and task-state tracking.

### MLflow (`citi_mlflow`)
Experiment tracking and model artifact management service. It records runs, parameters, metrics, and artifacts for ML-oriented exercises and model lifecycle demos.

## Observability Services

### Elasticsearch (`de_elasticsearch`)
Search and analytics engine for indexed logs/documents with fast query capabilities. It powers observability/search use cases and integrates with Kibana for dashboards.

### Kibana (`de_kibana`)
Visualization and dashboard layer for Elasticsearch data. It is used to explore indexed logs/metrics and build operational monitoring views.

### Splunk (`citi_splunk`)
Observability and log analytics platform for indexed machine and event data. It supports ingestion, search (SPL), and monitoring workflows commonly used in enterprise environments.

## How To Use This Dictionary
- Start/stop services with `_infra/scripts/infra_up.ps1` and `_infra/scripts/infra_down.ps1`.
- Validate runtime state with `_infra/scripts/infra_health.ps1`.
- Keep service purpose updates in sync when compose services are added/renamed/removed.
