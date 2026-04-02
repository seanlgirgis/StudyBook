# Story:
# Log volume and error rates are monitored for anomalies.

BASELINE_REQUESTS = 100
BASELINE_ERRORS = 2

WINDOWS = [
    {"window": "10:00", "requests": 105, "errors": 1},
    {"window": "10:05", "requests": 98, "errors": 2},
    {"window": "10:10", "requests": 40, "errors": 1},
    {"window": "10:15", "requests": 120, "errors": 9},
]


def detect_anomalies(windows):
    anomalies = []
    for w in windows:
        if w["requests"] < BASELINE_REQUESTS * 0.6:
            anomalies.append({"window": w["window"], "type": "throughput_drop"})
        if w["errors"] > BASELINE_ERRORS * 3:
            anomalies.append({"window": w["window"], "type": "error_spike"})
    return anomalies


def run_log_anomaly_demo():
    print("=" * 72)
    print("Scenario: log-based anomaly detection")

    print("\nBaseline")
    print({"requests": BASELINE_REQUESTS, "errors": BASELINE_ERRORS})

    print("\nWindows")
    for w in WINDOWS:
        print(f"  {w}")

    anomalies = detect_anomalies(WINDOWS)
    print("\nAnomalies")
    for a in anomalies:
        print(f"  {a}")

    print("\nSummary")
    print("- Drops in throughput and spikes in errors are anomalies.")
    print("- Thresholds catch unusual log patterns.")


if __name__ == "__main__":
    run_log_anomaly_demo()

# Takeaway: Simple baselines help flag log anomalies quickly.
