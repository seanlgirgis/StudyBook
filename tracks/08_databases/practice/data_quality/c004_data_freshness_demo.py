# Story:
# A daily feed should arrive by 08:00. Freshness checks compare the latest
# load timestamp to the expected window and flag stale data.

EXPECTED_ARRIVAL_HOUR = 8

FRESH_BATCH = {
    "batch_id": "2026-03-27",
    "loaded_at": "2026-03-27 07:45",
    "rows": 1200,
}

STALE_BATCH = {
    "batch_id": "2026-03-26",
    "loaded_at": "2026-03-27 10:30",
    "rows": 1180,
}


def _parse_hour(timestamp_text):
    date_part, time_part = timestamp_text.split(" ")
    hour_text, _minute = time_part.split(":")
    return int(hour_text)


def check_freshness(batch):
    loaded_hour = _parse_hour(batch["loaded_at"])
    is_fresh = loaded_hour <= EXPECTED_ARRIVAL_HOUR
    return {
        "batch_id": batch["batch_id"],
        "loaded_at": batch["loaded_at"],
        "loaded_hour": loaded_hour,
        "expected_by": f"{EXPECTED_ARRIVAL_HOUR:02d}:00",
        "status": "PASS" if is_fresh else "FAIL",
    }


def run_data_freshness_demo():
    print("=" * 72)
    print("Scenario: data freshness checks")

    print("\nExpected arrival window: by 08:00")

    print("\nFresh batch")
    fresh_result = check_freshness(FRESH_BATCH)
    print(fresh_result)

    print("\nStale batch")
    stale_result = check_freshness(STALE_BATCH)
    print(stale_result)

    print("\nSummary")
    print("- Freshness checks compare load time to an expected window.")
    print("- Late arrivals are flagged as stale.")


if __name__ == "__main__":
    run_data_freshness_demo()

# Takeaway: Freshness checks detect late-arriving data.
