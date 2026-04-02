# Story:
# A pipeline ingests events with event_time. A watermark says how late data can be.
# A high-water mark is the last event_time successfully processed.

EVENTS = [
    {"event_id": "e1", "event_time": "10:00", "value": 10},
    {"event_id": "e2", "event_time": "10:05", "value": 20},
    {"event_id": "e3", "event_time": "10:02", "value": 15},
    {"event_id": "e4", "event_time": "09:55", "value": 8},
    {"event_id": "e5", "event_time": "10:07", "value": 12},
]

LATE_TOLERANCE_MINUTES = 5


def _minutes(time_text):
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def _print_events(label, rows):
    print(label)
    for row in rows:
        print(f"  {row}")


def process_events(events):
    # Simulate processing in arrival order with watermark and high-water mark.
    max_event_time = None
    high_water_mark = None
    accepted = []
    rejected = []

    for event in events:
        event_time = _minutes(event["event_time"])
        max_event_time = event_time if max_event_time is None else max(max_event_time, event_time)
        watermark = max_event_time - LATE_TOLERANCE_MINUTES

        is_late = event_time < watermark
        if is_late:
            rejected.append({"event": event, "reason": f"late (watermark {watermark})"})
            print(
                f"[DROP] {event['event_id']} event_time={event_time} "
                f"watermark={watermark} max_event_time={max_event_time}"
            )
            continue

        accepted.append(event)
        high_water_mark = event_time if high_water_mark is None else max(high_water_mark, event_time)
        print(
            f"[ACCEPT] {event['event_id']} event_time={event_time} "
            f"watermark={watermark} high_water_mark={high_water_mark}"
        )

    return accepted, rejected, high_water_mark, max_event_time


def run_watermark_demo():
    print("=" * 72)
    print("Scenario: watermarks vs high-water marks")
    _print_events("Arrival order:", EVENTS)

    accepted, rejected, high_water_mark, max_event_time = process_events(EVENTS)

    print("\nAccepted events:")
    _print_events("", accepted)
    print("Rejected events:")
    for item in rejected:
        print(f"  {item}")

    final_watermark = max_event_time - LATE_TOLERANCE_MINUTES

    print("\nSummary")
    print(f"Final high-water mark: {high_water_mark}")
    print(f"Final watermark: {final_watermark}")
    print("- High-water mark = last processed event_time.")
    print("- Watermark = cutoff for late data (max_event_time - tolerance).")


if __name__ == "__main__":
    run_watermark_demo()

# Takeaway: High-water mark tracks processed progress; watermark limits late arrivals.
