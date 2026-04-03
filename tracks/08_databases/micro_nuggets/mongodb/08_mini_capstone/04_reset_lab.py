"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CAPSTONE 04 · Reset Lab                                                     ║
║  Clean up all MongoDB nugget collections to start fresh.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Drop all collections created by the MongoDB nuggets so you can re-run
the full series from a clean state.

USAGE
─────
    python 04_reset_lab.py

EXPECTED OUTPUT
───────────────
    ── CAPSTONE 04 · Reset Lab ──────────────────────

      Collections in nugget_lab before reset: 18

      Dropping: articles ............... OK
      Dropping: catalog ................. OK
      ...

      nugget_lab is now empty. Ready to re-run nuggets from 00_setup/.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

client = get_client()
db     = client[LAB_DB]

print("\n── CAPSTONE 04 · Reset Lab ──────────────────────")

collections = db.list_collection_names()
print(f"\n  Collections in {LAB_DB} before reset: {len(collections)}")

if not collections:
    print(f"\n  Nothing to drop — {LAB_DB} is already empty.")
else:
    for col_name in sorted(collections):
        print(f"  Dropping: {col_name:<35}", end="", flush=True)
        try:
            db.drop_collection(col_name)
            print(" OK")
        except Exception as e:
            print(f" ERROR: {e}")

remaining = db.list_collection_names()
if not remaining:
    print(f"\n  {LAB_DB} is now empty. Ready to re-run nuggets from 00_setup/.")
else:
    print(f"\n  {len(remaining)} collections remain: {remaining}")

client.close()
print()
