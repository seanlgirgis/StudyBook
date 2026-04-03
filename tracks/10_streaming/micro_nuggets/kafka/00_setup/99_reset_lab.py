"""
+==============================================================================+
|  NUGGET 00-99 . Reset Lab                                                    |
|  Delete all lab topics and return to a clean state.                          |
+==============================================================================+

PURPOSE
-------
  Delete all topics in LAB_TOPICS, then optionally re-seed via 01_seed_lab.py.
  Only affects lab.* topics -- system topics (__consumer_offsets etc.) are
  never touched.

SAFETY
------
  - Requires --confirm flag to prevent accidental deletion.
  - Does NOT stop Docker containers.
  - Does NOT affect non-lab topics.

USAGE
-----
    python 99_reset_lab.py --confirm        # delete lab topics
    python 99_reset_lab.py --confirm --reseed  # delete then re-seed
    python 99_reset_lab.py --dry-run        # preview without deleting
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, LAB_TOPICS, require_broker

parser = argparse.ArgumentParser(description="Reset Kafka lab topics.")
parser.add_argument("--confirm", action="store_true", help="Required: actually delete topics.")
parser.add_argument("--reseed", action="store_true", help="Re-create and re-seed after deletion.")
parser.add_argument("--dry-run", action="store_true", help="Preview topics that would be deleted.")
args = parser.parse_args()

require_broker(BROKER)

from kafka import KafkaAdminClient, KafkaConsumer

print("\n-- Kafka Lab Reset --")
print(f"  Broker: {BROKER}")
print()

# List existing lab topics
admin = KafkaAdminClient(bootstrap_servers=BROKER, request_timeout_ms=15_000)
all_topics = set(KafkaConsumer(bootstrap_servers=BROKER, consumer_timeout_ms=2_000).topics())
lab_present = [t for t in LAB_TOPICS if t in all_topics]

if not lab_present:
    print("  No lab topics found. Nothing to reset.")
    admin.close()
    sys.exit(0)

print(f"  Lab topics found ({len(lab_present)}):")
for t in sorted(lab_present):
    print(f"    {t}")
print()

if args.dry_run:
    print("  [DRY RUN] Topics listed above would be deleted.")
    print("  Re-run with --confirm to actually delete.")
    admin.close()
    sys.exit(0)

if not args.confirm:
    print("  Aborting: --confirm flag is required to delete topics.")
    print("  Re-run with:  python 99_reset_lab.py --confirm")
    admin.close()
    sys.exit(1)

# Delete
print("  Deleting lab topics ...")
try:
    result = admin.delete_topics(lab_present, timeout_ms=30_000)
    for topic, error in result.topic_error_codes:
        if error == 0:
            print(f"    [DELETED] {topic}")
        else:
            print(f"    [WARN]    {topic} -- error code {error}")
except Exception as exc:
    print(f"  [ERROR] {exc}")
    admin.close()
    sys.exit(1)

admin.close()

# Brief pause for broker to fully process deletion
time.sleep(3)

print()
print("  Lab topics deleted.")

if args.reseed:
    print()
    print("  Re-seeding lab ...")
    import subprocess
    seed_script = Path(__file__).parent / "01_seed_lab.py"
    result = subprocess.run([sys.executable, str(seed_script)], check=False)
    if result.returncode != 0:
        print("  [WARN] Re-seed returned non-zero exit code.")
    else:
        print("  Re-seed complete.")
else:
    print()
    print("  To recreate topics and seed data, run:")
    print("    python 01_seed_lab.py")

print()
