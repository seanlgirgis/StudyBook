# Story:
# The dashboard looks wrong because upstream data stopped arriving.
# dbt sources + freshness checks catch stale data before reports drift.

from datetime import datetime


CURRENT_TIME = "2024-02-02 09:00"
FRESHNESS_RULE = {
    "warn_after_hours": 2,
    "error_after_hours": 6,
}

SOURCES = [
    {
        "name": "payments_api_daily",
        "latest_loaded_at": "2024-02-02 08:30",
        "schedule": "daily 06:00",
    },
    {
        "name": "crm_accounts_daily",
        "latest_loaded_at": "2024-02-02 06:30",
        "schedule": "daily 06:00",
    },
    {
        "name": "shipping_events_daily",
        "latest_loaded_at": "2024-02-01 22:00",
        "schedule": "daily 06:00",
    },
]


def _parse_time(raw_value):
    return datetime.strptime(raw_value, "%Y-%m-%d %H:%M")


def _lag_hours(current_time, latest_time):
    delta = current_time - latest_time
    return round(delta.total_seconds() / 3600, 2)


def _freshness_status(lag_hours, warn_after, error_after):
    if lag_hours <= warn_after:
        return "fresh"
    if lag_hours <= error_after:
        return "warning"
    return "stale"


def _print_source_status(source, current_time, lag_hours, status):
    print(f"Source: {source['name']} (schedule: {source['schedule']})")
    print(f"- Latest data timestamp: {source['latest_loaded_at']}")
    print(f"- Current time: {current_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"- Lag hours: {lag_hours}")
    print(f"- Freshness status: {status}")


def run_sources_freshness_demo():
    print("=" * 72)
    print("Scenario: daily upstream feeds power revenue dashboards")
    print("Source = the upstream system you depend on.")
    print("Freshness = how recent the latest data is vs expectation.")

    current_time = _parse_time(CURRENT_TIME)
    warn_after = FRESHNESS_RULE["warn_after_hours"]
    error_after = FRESHNESS_RULE["error_after_hours"]

    print("=" * 72)
    print("Freshness rule: data must arrive within X hours of schedule")
    print(f"Warning after {warn_after} hours, stale after {error_after} hours.")

    print("=" * 72)
    print("Checking sources...")
    for source in SOURCES:
        latest_time = _parse_time(source["latest_loaded_at"])
        lag = _lag_hours(current_time, latest_time)
        status = _freshness_status(lag, warn_after, error_after)
        _print_source_status(source, current_time, lag, status)
        if status == "stale":
            print("- Risk: dashboards will be wrong until this source catches up.")
        elif status == "warning":
            print("- Risk: borderline freshness; investigate delays.")
        print("-")

    print("=" * 72)
    print("Summary:")
    print("- Sources are upstream systems you depend on.")
    print("- Freshness compares latest data time to expected arrival.")
    print("- Fresh/warning/stale signals let you catch late data early.")


if __name__ == "__main__":
    run_sources_freshness_demo()

# Takeaway: Freshness checks turn late upstream data into a visible, actionable signal.