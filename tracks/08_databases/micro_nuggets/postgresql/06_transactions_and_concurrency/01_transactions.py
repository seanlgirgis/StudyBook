"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-01 · Transactions, Isolation & Deadlocks                          ║
║  ACID properties in action.                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates transactions, isolation levels, and deadlock prevention.

CONCEPTS
────────
ACID:
  - Atomicity: all or nothing — no partial commits.
  - Consistency: database moves from one valid state to another.
  - Isolation: concurrent transactions don't interfere.
  - Durability: committed data survives crashes.

Isolation levels (PostgreSQL):
  - Read Committed (default): each query sees data committed before it started.
    Non-repeatable reads possible (same query returns different results).
  - Repeatable Read: entire transaction sees a consistent snapshot.
    Phantom reads possible (new rows appear between queries).
  - Serializable: strictest — behaves as if transactions ran one at a time.
    May abort transactions with serialization failures.

Deadlocks:
  - Two transactions each hold a lock the other needs.
  - PostgreSQL detects deadlocks and aborts one transaction.
  - Prevention: always lock resources in the same order.

USAGE
─────
    python 01_transactions.py

EXPECTED OUTPUT
───────────────
    ── Transactions & Isolation ──────────────────────────────

      ── Atomicity Demo ────────────────────────────────────
        [✓] ROLLBACK prevented partial update

      ── Isolation Level Demo ──────────────────────────────
        Read Committed: sees committed data
        Repeatable Read: consistent snapshot

      ── Deadlock Prevention ───────────────────────────────
        Lock resources in consistent order to avoid deadlocks
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Transactions & Isolation ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Atomicity — ROLLBACK undoes all changes in the transaction
#    This is the "A" in ACID. Either everything commits or nothing does.
#    Real-world use: money transfers, order processing, multi-table updates.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Atomicity Demo ────────────────────────────────────")
with conn.cursor() as cur:
    # Get initial balance
    cur.execute(f"""
        SELECT COALESCE(SUM(CASE WHEN txn_type = 'credit' THEN amount
                                 ELSE -amount END), 0)
        FROM {LAB_SCHEMA}.transactions WHERE account_id = 1
    """)
    initial = cur.fetchone()[0]

    # Start a transaction, make changes, then ROLLBACK
    cur.execute("BEGIN")
    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.transactions (account_id, amount, txn_type)
        VALUES (1, 1000, 'credit')
    """)
    cur.execute("ROLLBACK")

    # Verify the insert was undone
    cur.execute(f"""
        SELECT COALESCE(SUM(CASE WHEN txn_type = 'credit' THEN amount
                                 ELSE -amount END), 0)
        FROM {LAB_SCHEMA}.transactions WHERE account_id = 1
    """)
    after = cur.fetchone()[0]

    if initial == after:
        print("    [✓] ROLLBACK prevented partial update")
    else:
        print(f"    [✗] ROLLBACK failed: {initial} → {after}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Isolation levels — demonstrate Read Committed vs Repeatable Read
#    In Read Committed (default), each query sees the latest committed data.
#    In Repeatable Read, the entire transaction sees a consistent snapshot.
#
#    We can't fully demo concurrent behavior in a single-threaded script,
#    but we can show how to SET the isolation level.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Isolation Level Demo ──────────────────────────────")

# Read Committed (default)
conn2 = get_connection()
with conn2.cursor() as cur:
    cur.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.orders")
    count1 = cur.fetchone()[0]
    print(f"    Read Committed: {count1} orders")
conn2.close()

# Repeatable Read
conn3 = get_connection()
with conn3.cursor() as cur:
    cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.orders")
    count2 = cur.fetchone()[0]
    print(f"    Repeatable Read: {count2} orders (consistent snapshot)")
conn3.close()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Deadlock prevention — the golden rule
#    Always lock resources in the SAME ORDER.
#    If Transaction A locks row 1 then row 2, and Transaction B locks row 2
#    then row 1, they'll deadlock.
#
#    Prevention: establish a convention (e.g., always lock by ascending ID).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Deadlock Prevention ───────────────────────────────")
print("    Golden rule: always lock resources in consistent order.")
print("    Example: UPDATE accounts WHERE id IN (1, 2, 3) — sorted ascending.")
print("    PostgreSQL detects deadlocks and aborts one transaction.")

conn.close()
print()
