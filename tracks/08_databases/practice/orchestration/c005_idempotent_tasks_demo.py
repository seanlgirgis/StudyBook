# Story:
# A pipeline retries and backfills the same day. Without idempotency, results duplicate.


def _print_table(label, table):
    print(label)
    for date_label, rows in sorted(table.items()):
        print(f"- {date_label}: {rows}")


def _non_idempotent_load(table, date_label, events):
    table.setdefault(date_label, [])
    table[date_label].extend(events)


def _idempotent_load_by_partition(table, date_label, events):
    deduped = []
    seen = set()
    for event in events:
        if event["event_id"] not in seen:
            seen.add(event["event_id"])
            deduped.append(event)
    table[date_label] = deduped


def run_idempotent_tasks_demo():
    print("=" * 72)
    print("Scenario: daily event ingestion with retries and backfills")
    print("Non-idempotent = run again changes the result.")
    print("Idempotent = run again leaves the final result the same.")

    events_0103 = [
        {"event_id": "e1", "amount": 50},
        {"event_id": "e2", "amount": 90},
    ]

    print("=" * 72)
    print("Case A: non-idempotent task (duplicates on retry)")
    non_idempotent_table = {}
    _non_idempotent_load(non_idempotent_table, "2024-01-03", events_0103)
    _print_table("After first run:", non_idempotent_table)

    print("[RETRY] task reruns due to a transient failure")
    _non_idempotent_load(non_idempotent_table, "2024-01-03", events_0103)
    _print_table("After retry (duplicates):", non_idempotent_table)

    print("=" * 72)
    print("Case B: idempotent task (overwrite + dedup by event_id)")
    idempotent_table = {}
    _idempotent_load_by_partition(idempotent_table, "2024-01-03", events_0103)
    _print_table("After first run:", idempotent_table)

    print("[RETRY] task reruns due to a transient failure")
    _idempotent_load_by_partition(idempotent_table, "2024-01-03", events_0103)
    _print_table("After retry (same result):", idempotent_table)

    print("=" * 72)
    print("Case C: backfill rerun over an already-processed interval")
    _idempotent_load_by_partition(idempotent_table, "2024-01-02", [{"event_id": "e9", "amount": 20}])
    _print_table("Before backfill rerun:", idempotent_table)

    print("[BACKFILL] reprocess 2024-01-02 safely")
    _idempotent_load_by_partition(idempotent_table, "2024-01-02", [{"event_id": "e9", "amount": 20}])
    _print_table("After backfill rerun (unchanged):", idempotent_table)

    print("=" * 72)
    print("Summary:")
    print("- Non-idempotent tasks duplicate or corrupt results on rerun.")
    print("- Idempotent tasks use safe mechanisms like overwrite + dedup.")
    print("- Retries and backfills depend on idempotent behavior.")


if __name__ == "__main__":
    run_idempotent_tasks_demo()

# Takeaway: Idempotency lets retries and backfills rerun safely without changing results.
