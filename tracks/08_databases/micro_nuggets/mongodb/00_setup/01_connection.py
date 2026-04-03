"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Basic Connection                                             ║
║  The minimal pattern every other nugget builds on.                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Opens a MongoClient, pings the cluster, lists databases, closes cleanly.
This is the smallest possible working program — learn this shape first.

CONCEPTS
────────
MongoClient:
  - The entry point to every MongoDB operation in pymongo.
  - Maintains an internal connection pool (default maxPoolSize=100).
  - Thread-safe — one client per process is the correct pattern.
  - Connections are established lazily: constructing MongoClient does NOT
    immediately open a socket. The first actual operation does.
  - This is different from Snowflake/Databricks where connect() blocks
    until a session is established.

Database and Collection:
  - client["db_name"]         → Database object (no network call)
  - db["collection_name"]     → Collection object (no network call)
  - Both are lightweight Python references — cheap to create at any time.
  - The actual database/collection is created on first write (MongoDB
    creates namespaces on demand — no CREATE DATABASE / CREATE TABLE needed).

admin.command("ping"):
  - The canonical way to test server reachability in MongoDB.
  - Returns {"ok": 1.0} on success.
  - Requires no special permissions — any authenticated user can ping.
  - This is synchronous: it blocks until the server responds or timeout fires.

list_database_names():
  - Returns the list of databases the current user can see.
  - Requires the "listDatabases" privilege on the "admin" database.
  - On Atlas, this works out of the box for the admin user.
  - Note: databases appear here only if they contain at least one collection.

Connection lifecycle for scripts:
  - Open client → do work → close client.
  - Don't hold MongoClient open across long waits (idle connections
    consume Atlas cluster resources and may be closed by the server).
  - For web services: create ONE MongoClient at startup, share it globally.

USAGE
─────
    python 01_connection.py

EXPECTED OUTPUT
───────────────
    ── MongoDB Connection ─────────────────────────

      Ping response:  {'ok': 1.0}
      Databases:      ['de_telemetry', 'sample_mflix', 'admin', 'local', 'nugget_lab']
      Lab DB:         nugget_lab  (will be created on first write)

      Connection closed cleanly.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

# ─────────────────────────────────────────────────────────────────────────────
# Open the client
# get_client() reads credentials, builds the URI, and returns a MongoClient.
# No socket is opened yet — that happens on the next line (admin.command).
# ─────────────────────────────────────────────────────────────────────────────
client = get_client()

print("\n── MongoDB Connection ─────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Ping — triggers the first actual network round-trip.
# After this succeeds, subsequent calls reuse the pool connection (~5-10 ms).
# ─────────────────────────────────────────────────────────────────────────────
ping = client.admin.command("ping")
print(f"\n  Ping response:  {ping}")

# ─────────────────────────────────────────────────────────────────────────────
# List databases
# nugget_lab may not appear yet if it has no collections — that is normal.
# MongoDB creates the database the first time you insert a document into it.
# ─────────────────────────────────────────────────────────────────────────────
dbs = client.list_database_names()
print(f"  Databases:      {dbs}")
print(f"  Lab DB:         {LAB_DB}  (will be created on first write if absent)")

# ─────────────────────────────────────────────────────────────────────────────
# Close — drains the connection pool gracefully.
# For scripts that exit immediately after, this is optional (Python's GC
# handles it), but it is good practice and prevents ResourceWarning logs.
# ─────────────────────────────────────────────────────────────────────────────
client.close()
print("\n  Connection closed cleanly.")
print()
