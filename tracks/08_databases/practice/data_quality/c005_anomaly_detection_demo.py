# Story:
# A pipeline monitors daily revenue totals. A baseline range flags outliers.
# Obvious spikes are anomalies; normal totals pass.

BASELINE_AVG = 1000
BASELINE_TOLERANCE = 200

OUTLIER_DAY = {
    "date": "2026-03-27",
    "revenue": 2400,
}

NORMAL_DAY = {
    "date": "2026-03-28",
    "revenue": 980,
}


def check_anomaly(day, avg, tolerance):
    lower = avg - tolerance
    upper = avg + tolerance
    status = "PASS" if lower <= day["revenue"] <= upper else "FAIL"
    return {
        "date": day["date"],
        "revenue": day["revenue"],
        "baseline": f"{lower}-{upper}",
        "status": status,
    }


def run_anomaly_detection_demo():
    print("=" * 72)
    print("Scenario: anomaly detection basics")
    print(f"Baseline average: {BASELINE_AVG}, tolerance: {BASELINE_TOLERANCE}")

    print("\nOutlier day")
    outlier_result = check_anomaly(OUTLIER_DAY, BASELINE_AVG, BASELINE_TOLERANCE)
    print(outlier_result)

    print("\nNormal day")
    normal_result = check_anomaly(NORMAL_DAY, BASELINE_AVG, BASELINE_TOLERANCE)
    print(normal_result)

    print("\nSummary")
    print("- Baseline ranges flag unusual spikes or drops.")
    print("- Outliers fail; normal values pass.")


if __name__ == "__main__":
    run_anomaly_detection_demo()

# Takeaway: Simple baselines catch obvious anomalies.
