"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-01 · Multi-Document Transactions                                  ║
║  ACID guarantees across multiple documents and collections.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Use MongoDB multi-document transactions to perform ACID operations across
multiple collections — the same guarantee as a SQL database transaction.

CONCEPTS
────────
MongoDB Transaction History:
  - MongoDB is ACID at the SINGLE-DOCUMENT level since its inception.
    A single document update (including embedded arrays) is always atomic.
  - Multi-document ACID transactions were added in MongoDB 4.0 (replica sets)
    and 4.2 (sharded clusters).
  - Atlas always runs as a replica set → multi-doc transactions are always available.

When you need transactions:
  - Transferring value between two documents (e.g., account balances).
  - Creating an order AND decrementing inventory atomically.
  - Any operation that must leave the database consistent across multiple docs.
  - When NOT to use: single-document operations already provide ACID.
    Transactions add latency and overhead — use only when necessary.

Session and Transaction API:
  client.start_session()                → creates a ClientSession object.
  session.start_transaction()           → opens the transaction.
  session.commit_transaction()          → atomically commits.
  session.abort_transaction()           → rolls back.
  session.with_transaction(callback)    → recommended! Auto-retry on transient errors.

with_transaction(callback, read_preference=..., write_concern=..., ...):
  - The callback receives the session as its argument.
  - Automatically retries on TransientTransactionError (e.g., network blip).
  - Automatically retries commit on UnknownTransactionCommitResult.
  - The retry loop is mandatory for production — transient errors are common
    on Atlas due to maintenance, elections, and cross-shard routing.
  - The callback must be IDEMPOTENT (side-effect-free) because it may run
    multiple times on retry.

Transaction constraints:
  - Max transaction duration: 60 seconds (configurable, Atlas default: 60s).
  - Max document size per transaction: limited by WiredTiger's cache.
  - Cross-collection OK. Cross-database OK. Cross-cluster: NOT supported.
  - Read your own writes: within a transaction, reads see uncommitted writes
    from the SAME transaction (snapshot isolation).

Read your own writes:
  Outside transactions, MongoDB's default read preference is PRIMARY with
  read concern "local" — you always read from primary, so you see your writes.
  Inside transactions, read concern "snapshot" is used by default, which
  provides a consistent point-in-time view of the data at transaction start.

USAGE
─────
    python 01_multi_doc_transaction.py

EXPECTED OUTPUT
───────────────
    ── Multi-Document Transactions ──────────────────

      Seeded accounts: Alice=$1000.00, Bob=$500.00

      Transfer $250 from Alice to Bob...
      [✓] Transfer committed. Alice=$750.00, Bob=$750.00

      Attempting invalid transfer (overdraft)...
      [✗] Transfer aborted: insufficient funds.
          Alice=$750.00 (unchanged), Bob=$750.00 (unchanged)
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo import WriteConcern, ReadPreference
from pymongo.read_concern import ReadConcern
from pymongo.errors import OperationFailure

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

client = get_client()
db     = client[LAB_DB]

print("\n── Multi-Document Transactions ──────────────────")

db.drop_collection("accounts")
db.drop_collection("txn_ledger")
accounts = db["accounts"]
ledger   = db["txn_ledger"]

# ─────────────────────────────────────────────────────────────────────────────
# Seed: two bank accounts
# ─────────────────────────────────────────────────────────────────────────────
accounts.insert_many([
    {"_id": "alice", "name": "Alice",  "balance": 1000.0, "currency": "USD"},
    {"_id": "bob",   "name": "Bob",    "balance":  500.0, "currency": "USD"},
])

def get_balance(name: str) -> float:
    doc = accounts.find_one({"_id": name})
    return doc["balance"] if doc else 0.0

print(f"\n  Seeded accounts: Alice=${get_balance('alice'):.2f}, Bob=${get_balance('bob'):.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# Transfer function — runs inside a transaction
# with_transaction will retry the entire callback on TransientTransactionError.
# The callback MUST be idempotent — don't do external side effects here.
# ─────────────────────────────────────────────────────────────────────────────
def transfer(session, from_id: str, to_id: str, amount: float, description: str = ""):
    """
    Atomically transfer 'amount' from 'from_id' to 'to_id'.
    Both the account balances AND the ledger entry update in one transaction.
    """
    # Step 1: Check source has sufficient funds
    # Pass session= to ALL operations inside the transaction.
    src = accounts.find_one({"_id": from_id}, session=session)
    if src is None:
        raise OperationFailure(f"Account '{from_id}' not found.")
    if src["balance"] < amount:
        raise OperationFailure(
            f"Insufficient funds: {from_id} has ${src['balance']:.2f}, "
            f"requested ${amount:.2f}"
        )

    # Step 2: Debit source
    accounts.update_one(
        {"_id": from_id},
        {"$inc": {"balance": -amount}},
        session=session,
    )

    # Step 3: Credit destination
    accounts.update_one(
        {"_id": to_id},
        {"$inc": {"balance": amount}},
        session=session,
    )

    # Step 4: Write audit ledger entry
    ledger.insert_one({
        "from":        from_id,
        "to":          to_id,
        "amount":      amount,
        "description": description,
        "ts":          datetime.now(tz=timezone.utc),
    }, session=session)

    # No commit here — with_transaction handles it

# ─────────────────────────────────────────────────────────────────────────────
# Successful transfer: Alice → Bob $250
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Transfer $250 from Alice to Bob...")
try:
    with client.start_session() as session:
        session.with_transaction(
            lambda s: transfer(s, "alice", "bob", 250.0, "Payment for laptop"),
            # Production settings: majority write concern for durability
            write_concern=WriteConcern("majority"),
            read_concern=ReadConcern("snapshot"),
            read_preference=ReadPreference.PRIMARY,
        )
    print(f"  [✓] Transfer committed. "
          f"Alice=${get_balance('alice'):.2f}, Bob=${get_balance('bob'):.2f}")

except OperationFailure as e:
    print(f"  [✗] Transfer failed: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Failed transfer: overdraft attempt — Alice has $750, trying to send $900
# with_transaction aborts the transaction when the callback raises.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Attempting invalid transfer (overdraft)...")
try:
    with client.start_session() as session:
        session.with_transaction(
            lambda s: transfer(s, "alice", "bob", 900.0, "This should fail"),
            write_concern=WriteConcern("majority"),
        )
    print(f"  [✗] Should not reach here!")

except OperationFailure as e:
    msg = (e.details or {}).get("errmsg", str(e))[:60]
    print(f"  [✗] Transfer aborted: {msg}")
    print(f"      Alice=${get_balance('alice'):.2f} (unchanged), "
          f"Bob=${get_balance('bob'):.2f} (unchanged)")

# ─────────────────────────────────────────────────────────────────────────────
# Ledger audit — only the successful transfer is recorded
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Ledger entries (only committed transactions):")
for entry in ledger.find({}, {"_id": 0, "ts": 0}):
    print(f"    {entry['from']} → {entry['to']}  ${entry['amount']:.2f}  '{entry['description']}'")

# cleanup
db.drop_collection("accounts")
db.drop_collection("txn_ledger")
client.close()
print()
