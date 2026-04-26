# Docker Learning Pack For PySpark Tutorial

This folder is a teachable mini-course for using Docker with Spark in this tutorial.

## Start Here

1. [Why Docker For Spark?](./01_why_docker_for_spark.md)
2. [How To Build Images And Compose](./02_build_images.md)
3. [How To Deploy Locally](./03_deploy_local_compose.md)
4. [Why We Use Two Containers](./04_why_two_containers.md)
5. [How To Run This Tutorial Using The Containers](./05_run_tutorial_with_containers.md)
6. [Docker vs Local Spark](./06_docker_vs_local.md)
7. [Deploying To Cloud (AWS and others)](./07_deploy_on_cloud.md)

## Sample Files

- [docker-compose.spark-standalone.sample.yml](./samples/docker-compose.spark-standalone.sample.yml)
- [Dockerfile.pyspark-client.sample](./samples/Dockerfile.pyspark-client.sample)
- [.env.sample](./samples/.env.sample)
- [run_tutorial_local.ps1](./samples/run_tutorial_local.ps1)
- [run_tutorial_in_client_container.sh](./samples/run_tutorial_in_client_container.sh)

## How This Connects To Current Setup

Your current local cluster uses:

- `citi_spark` (master)
- `citi_spark_worker` (worker)

Tutorial scripts connect to master URL:

- `spark://localhost:7077`
