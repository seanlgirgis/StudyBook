# 07 - Deploying These Containers On Cloud

Back to [Docker Pack Index](./README.md)

## AWS options

1. ECS/Fargate (container-first)
- Good for managed container operations
- Deploy master + worker services
- Use load balancer/security groups for UI and driver access

2. EKS (Kubernetes)
- Best when you already run K8s
- Spark can run through Spark-on-K8s patterns

3. EMR (managed Spark, not raw container pair)
- Easiest managed Spark operations
- You usually submit Spark jobs to EMR rather than run this exact master/worker compose pair

## Other clouds

1. GCP
- GKE (Kubernetes route)
- Dataproc (managed Spark route)

2. Azure
- AKS (Kubernetes route)
- HDInsight / Synapse Spark (managed Spark route)

3. Databricks (AWS/Azure/GCP)
- Managed Spark platform
- You submit notebooks/jobs to managed clusters

## Key differences (local vs cloud)

- Networking:
  - local uses `localhost`
  - cloud uses private VPC/VNet DNS/IP and security rules
- Storage:
  - local disk/binds
  - cloud object storage (`S3`, `GCS`, `ADLS`)
- Auth:
  - local often none
  - cloud requires IAM/service identities and secret management

## How to run tutorial scripts against cloud Spark

Set the master URL in your driver environment:

```powershell
$env:SPARK_MASTER_URL="spark://<cloud-master-host>:7077"
python -u .\01_cluster_connection.py
```

If platform is managed Spark (EMR/Dataproc/Databricks), you usually adapt submission style:

- submit jobs to platform runtime
- store data in cloud storage
- map configs to platform-native settings

## Migration recommendation

- First milestone: keep same scripts, move to container service (ECS/GKE/AKS) with minimal code change.
- Second milestone: adopt managed Spark platform for ops simplicity.
