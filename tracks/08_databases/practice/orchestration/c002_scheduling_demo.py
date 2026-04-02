# Story:
# The pipeline "should run at 2 AM," but nothing happens unless the trigger condition is met.


def _run(task, reason, time):
    print(f"[RUN] {task} at {time} because {reason}")


def _schedule_check(task, trigger_ok, time, expected_note):
    print(f"[SCHEDULE CHECK] {task} at {time}")
    if trigger_ok:
        _run(task, "schedule + trigger met", time)
        return True
    print(f"[NO RUN] {task} {expected_note}")
    return False


def run_scheduling_demo():
    print("=" * 72)
    print("Scenario: a reporting pipeline with schedules and triggers")
    print("Schedule = when the system checks or launches.")
    print("Trigger = the condition that actually causes execution.")

    print("=" * 72)
    print("Tasks:")
    print("- refresh_dashboard (time-based schedule)")
    print("- ingest_clickstream (event-based trigger)")
    print("- daily_snapshot (time-based schedule + data-ready trigger)")

    timeline = ["01:00", "01:15", "01:30", "01:45", "02:00", "02:30", "03:00"]
    events = {
        "01:15": "clickstream_batch_arrived",
        "02:30": "warehouse_loaded",
    }
    manual_triggers = {"01:45": ["refresh_dashboard"]}
    schedule_checks = {"01:00", "02:00", "03:00"}

    state = {
        "warehouse_loaded": False,
        "fresh_extract_ready": True,
    }

    print("=" * 72)
    print("Timeline:")
    for time in timeline:
        print(f"\n-- {time} --")

        if time in events:
            event = events[time]
            print(f"[EVENT] {event}")
            if event == "clickstream_batch_arrived":
                _run("ingest_clickstream", "event trigger", time)
            if event == "warehouse_loaded":
                state["warehouse_loaded"] = True
                print("[STATE] warehouse_loaded = True")

        if time in manual_triggers:
            for task in manual_triggers[time]:
                _run(task, "manual trigger", time)

        if time in schedule_checks:
            _schedule_check(
                "refresh_dashboard",
                trigger_ok=state["fresh_extract_ready"],
                time=time,
                expected_note="did not run because the extract was not ready",
            )

            _schedule_check(
                "daily_snapshot",
                trigger_ok=state["warehouse_loaded"],
                time=time,
                expected_note="was expected but the warehouse load was not done",
            )

        if time == "02:00":
            state["fresh_extract_ready"] = False
            print("[STATE] fresh_extract_ready = False (next schedule will skip)")

        if time == "03:00":
            state["fresh_extract_ready"] = True
            print("[STATE] fresh_extract_ready = True (future schedules can run)")

    print("=" * 72)
    print("Summary:")
    print("- Schedules define when checks happen.")
    print("- Triggers define whether a run actually happens.")
    print("- The same task can run twice for different reasons (schedule vs manual).")


if __name__ == "__main__":
    run_scheduling_demo()

# Takeaway: Schedules set the clock; triggers decide if the task really runs.
