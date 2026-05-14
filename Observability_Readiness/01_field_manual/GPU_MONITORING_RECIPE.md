# GPU Monitoring Recipe

## Goal
Track utilization and saturation risk for accelerated workloads.

## Core Signals
- GPU utilization.
- Memory utilization and memory errors.
- Temperature/power throttling indicators.
- Queue/wait time for GPU-bound jobs.

## Minimal Recipe
- Expose GPU metrics (for example via DCGM exporter pattern).
- Scrape and visualize alongside job/workload metadata.
- Alert on sustained saturation, thermal throttling, and memory pressure.
- Correlate with application latency and throughput.

## What I Can Say In Interview
- “I understand the operational signal model for GPU workloads and can map it to proven capacity and telemetry practices.”

## Do Not Overclaim
- Avoid claiming deep production GPU platform operations if not yet owned.
