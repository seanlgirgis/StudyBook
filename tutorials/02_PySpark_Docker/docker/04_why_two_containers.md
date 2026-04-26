# 04 - Why We Use Two Containers

Back to [Docker Pack Index](./README.md)

## Why two containers?

You currently run:

- `citi_spark` (master)
- `citi_spark_worker` (worker)

They have different responsibilities.

## Master

- Schedules jobs
- Tracks executors and resources
- Exposes cluster UI

## Worker

- Runs tasks on partitions
- Uses executor process(es)
- Reports progress to master

## Why not just one?

A single master-only setup can connect, but distributed execution is limited or misleading.
For learning real Spark behavior (stages, tasks, shuffle across executors), master + worker is the useful minimum.

## Scaling

You can add more workers for parallelism:

- `citi_spark_worker_2`
- `citi_spark_worker_3`

Next: [How To Run This Tutorial Using The Containers](./05_run_tutorial_with_containers.md)
