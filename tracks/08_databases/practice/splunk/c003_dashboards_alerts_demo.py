# Story:
# A dashboard summarizes key signals, while alerts trigger on thresholds.

EVENTS = [
    {"service": "checkout", "level": "INFO", "latency_ms": 120},
    {"service": "checkout", "level": "INFO", "latency_ms": 140},
    {"service": "payments", "level": "ERROR", "latency_ms": 900},
    {"service": "payments", "level": "WARN", "latency_ms": 500},
]

LATENCY_THRESHOLD = 400
ERROR_THRESHOLD = 1


def dashboard_metrics(events):
    total = len(events)
    errors = sum(1 for e in events if e["level"] == "ERROR")
    avg_latency = sum(e["latency_ms"] for e in events) / total
    return {"total_events": total, "error_count": errors, "avg_latency_ms": round(avg_latency, 1)}


def alert_checks(events):
    errors = sum(1 for e in events if e["level"] == "ERROR")
    high_latency = [e for e in events if e["latency_ms"] > LATENCY_THRESHOLD]
    alerts = []
    if errors >= ERROR_THRESHOLD:
        alerts.append(f"ERROR_COUNT >= {ERROR_THRESHOLD}")
    if high_latency:
        alerts.append(f"LATENCY_SPIKE > {LATENCY_THRESHOLD}ms")
    return alerts, high_latency


def run_dashboards_alerts_demo():
    print("=" * 72)
    print("Scenario: dashboards and alerting patterns")

    print("\nDashboard summary")
    metrics = dashboard_metrics(EVENTS)
    print(metrics)

    print("\nAlert evaluation")
    alerts, spikes = alert_checks(EVENTS)
    print("Alerts:", alerts)
    print("High latency events:")
    for event in spikes:
        print(f"  {event}")

    print("\nSummary")
    print("- Dashboards roll up signals for quick health checks.")
    print("- Alerts trigger on thresholds or spikes.")


if __name__ == "__main__":
    run_dashboards_alerts_demo()

# Takeaway: Dashboards summarize; alerts notify when thresholds are breached.
