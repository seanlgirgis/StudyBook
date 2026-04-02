"""
Title
Merge / Upsert: Incremental Loads in One Pass

Story
A daily customer status feed arrives. The target table already has customers 101, 102, 103. In the incoming feed, customer_id 102 changes status to churned, and customer_id 104 is brand new.

Street-Level Mental Model
Think of a doorman with a guest list. If your name is already inside, your details get updated. If your name is new, you get added to the list.

Technical Meaning
The target table holds prior state. The source feed contains a mix of existing and new business keys. A merge/upsert compares rows by the match key first, then updates matched rows and inserts unmatched rows.

Why INSERT-only fails
INSERT-only blindly appends the feed. Existing keys like customer_id 102 get duplicated with conflicting values.

Why UPDATE-only fails
UPDATE-only changes rows that already exist. New keys like customer_id 104 never get inserted.

How MERGE / UPSERT works
For each source row, check the match key. If a target row exists, update it. If not, insert it as a new row.

Match key intuition
Use a stable business key such as customer_id, order_id, or product_id. It is how you decide whether a row is already present.

What this pattern is great at
Incremental loads, daily status feeds, and SCD Type 1 style refreshes.

What this pattern is bad at
Complex conflict rules, multi-table orchestration, or preserving full change history (use SCD Type 2 for that).

Takeaway
Merge/upsert is the default incremental load pattern: update existing rows and insert new rows in one deterministic pass.
"""


# Target rows represent the current stored state before the new feed arrives.
TARGET_ROWS = [
    {"customer_id": 101, "status": "active", "tier": "silver"},
    {"customer_id": 102, "status": "active", "tier": "gold"},
    {"customer_id": 103, "status": "paused", "tier": "silver"},
]

# Source rows represent the incoming feed with both existing and new business keys.
SOURCE_ROWS = [
    {"customer_id": 102, "status": "churned", "tier": "gold"},
    {"customer_id": 104, "status": "active", "tier": "bronze"},
]


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


# Insert-only assumes every source row is new, which duplicates existing keys.
def insert_only(target_rows, source_rows):
    return target_rows + source_rows


# Update-only assumes every source row already exists, which drops new keys.
def update_only(target_rows, source_rows):
    updated = [row.copy() for row in target_rows]
    lookup = {row["customer_id"]: row for row in updated}
    for row in source_rows:
        if row["customer_id"] in lookup:
            lookup[row["customer_id"]].update(row)
    return list(lookup.values())


# Merge/upsert checks the match key: update if matched, insert if not matched.
def merge_upsert(target_rows, source_rows):
    merged = {row["customer_id"]: row.copy() for row in target_rows}
    updated_ids = []
    inserted_ids = []

    for row in source_rows:
        key = row["customer_id"]
        if key in merged:
            # Match found -> update the existing target row.
            merged[key].update(row)
            updated_ids.append(key)
        else:
            # No match -> insert a new target row.
            merged[key] = row.copy()
            inserted_ids.append(key)

    return list(merged.values()), updated_ids, inserted_ids


def run_merge_upsert_demo():
    print("=" * 72)
    _print_rows("Initial target rows:", TARGET_ROWS)

    print("=" * 72)
    _print_rows("Incoming source rows:", SOURCE_ROWS)

    print("=" * 72)
    print("Scenario A: INSERT-only thinking (duplicates / stale values)")
    inserted = insert_only(TARGET_ROWS, SOURCE_ROWS)
    _print_rows("Insert-only result:", inserted)
    print("Problem: customer_id=102 appears twice with conflicting status.")

    print("=" * 72)
    print("Scenario B: UPDATE-only thinking (misses new rows)")
    updated = update_only(TARGET_ROWS, SOURCE_ROWS)
    _print_rows("Update-only result:", updated)
    print("Problem: customer_id=104 never appears.")

    print("=" * 72)
    print("Scenario C: MERGE / UPSERT")
    merged, updated_ids, inserted_ids = merge_upsert(TARGET_ROWS, SOURCE_ROWS)
    print("MATCHED -> UPDATE ids:", updated_ids)
    print("NOT MATCHED -> INSERT ids:", inserted_ids)

    print("=" * 72)
    _print_rows("Final merged target:", sorted(merged, key=lambda r: r["customer_id"]))

    print("=" * 72)
    print("Interpretation:")
    print("- INSERT-only failed because existing rows were duplicated.")
    print("- UPDATE-only failed because new rows were lost.")
    print("- MERGE/UPSERT updated 102 and inserted 104 in one pass.")


if __name__ == "__main__":
    run_merge_upsert_demo()
