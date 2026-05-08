"""
Vanilla Python grouping demo.

This is useful for understanding the logic behind groupby.
In production, I would usually use Pandas, PySpark, or SQL for larger telemetry data.
"""

# Small in-memory telemetry sample (no DB, no file writes, no dependencies)
telemetry_rows = [
    {"service_name": "payments-api", "cpu_utilization_pct": 92, "memory_utilization_pct": 78, "p95_latency_ms": 380, "cloud_cost_usd": 11.2},
    {"service_name": "payments-api", "cpu_utilization_pct": 84, "memory_utilization_pct": 74, "p95_latency_ms": 420, "cloud_cost_usd": 10.7},
    {"service_name": "risk-engine", "cpu_utilization_pct": 31, "memory_utilization_pct": 40, "p95_latency_ms": 310, "cloud_cost_usd": 6.1},
    {"service_name": "risk-engine", "cpu_utilization_pct": 29, "memory_utilization_pct": 42, "p95_latency_ms": 330, "cloud_cost_usd": 6.4},
    {"service_name": "analytics-batch", "cpu_utilization_pct": 58, "memory_utilization_pct": 60, "p95_latency_ms": 470, "cloud_cost_usd": 9.8},
]

# Group rows by service_name
by_service = {}
for row in telemetry_rows:
    service = row["service_name"]
    by_service.setdefault(service, []).append(row)


# Build summary metrics per service
summaries = []
for service_name, rows in by_service.items():
    sample_count = len(rows)

    cpu_vals = [r["cpu_utilization_pct"] for r in rows]
    mem_vals = [r["memory_utilization_pct"] for r in rows]
    lat_vals = [r["p95_latency_ms"] for r in rows]
    cost_vals = [r["cloud_cost_usd"] for r in rows]

    avg_cpu_pct = sum(cpu_vals) / sample_count
    max_cpu_pct = max(cpu_vals)
    avg_memory_pct = sum(mem_vals) / sample_count
    max_memory_pct = max(mem_vals)
    avg_p95_latency_ms = sum(lat_vals) / sample_count
    total_cloud_cost_usd = sum(cost_vals)

    # Simple status logic
    if max_cpu_pct >= 90 or max_memory_pct >= 90:
        capacity_status = "high_capacity_risk"
    elif avg_cpu_pct < 35 and avg_memory_pct < 45:
        capacity_status = "rightsizing_candidate"
    elif avg_p95_latency_ms >= 450:
        capacity_status = "latency_watch"
    else:
        capacity_status = "normal"

    summaries.append(
        {
            "service_name": service_name,
            "sample_count": sample_count,
            "avg_cpu_pct": round(avg_cpu_pct, 2),
            "max_cpu_pct": round(max_cpu_pct, 2),
            "avg_memory_pct": round(avg_memory_pct, 2),
            "max_memory_pct": round(max_memory_pct, 2),
            "avg_p95_latency_ms": round(avg_p95_latency_ms, 2),
            "total_cloud_cost_usd": round(total_cloud_cost_usd, 2),
            "capacity_status": capacity_status,
        }
    )

# Print clean summary list
summaries.sort(key=lambda x: x["service_name"])
print("Service capacity summaries (vanilla Python):")
for s in summaries:
    print(s)
