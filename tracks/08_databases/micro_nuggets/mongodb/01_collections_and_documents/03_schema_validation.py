"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-03 · Schema Validation                                            ║
║  Enforcing structure in a "schema-less" database.                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Apply a JSON Schema validator to a collection to enforce data quality.
This is MongoDB's built-in schema enforcement — no ORM required.

CONCEPTS
────────
MongoDB JSON Schema Validator:
  - MongoDB 3.6+ supports $jsonSchema as a collection-level validator.
  - The schema follows the JSON Schema Draft 4 spec with MongoDB extensions.
  - Applied on INSERT and UPDATE operations.
  - Does NOT retroactively validate existing documents.

Create collection with validator:
  db.create_collection("name", validator={"$jsonSchema": {...}})

Or add/update validator on an existing collection:
  db.command("collMod", "name", validator={"$jsonSchema": {...}})

JSON Schema keywords used here:
  bsonType:    MongoDB-specific type name (use instead of "type").
               Values: "object", "array", "string", "int", "long",
                       "double", "decimal", "bool", "date", "objectId", "null"
  required:    List of fields that must be present.
  properties:  Shape of each field (type, description, constraints).
  minimum/maximum:    Numeric bounds.
  minLength/maxLength: String length bounds.
  enum:        Allowed values list.
  items:       Schema for array elements.
  additionalProperties: false → reject documents with undeclared fields.

validationLevel:
  "strict"   → validate on INSERT and UPDATE (default).
  "moderate" → validate on INSERT; only validate UPDATEs if the doc
               currently passes the validator. Useful during migrations.
  "off"      → disable validation entirely.

validationAction:
  "error"  → reject invalid writes with a WriteError (default).
  "warn"   → log a warning but allow the write. For soft migration.

USAGE
─────
    python 03_schema_validation.py

EXPECTED OUTPUT
───────────────
    ── Schema Validation ──────────────────────────────

      Created validated 'sensors' collection.

      [✓] Valid document inserted: sensor-001
      [✗] Missing required 'location':
          Document failed validation
      [✗] Invalid type for 'temperature' (string instead of double):
          Document failed validation
      [✗] Status out of enum: 'broken' not in ['active', 'inactive', 'maintenance']:
          Document failed validation
      [✓] Moderate validation — old invalid doc updated without error.

      Validator rules for 'sensors':
        required: ['sensor_id', 'location', 'temperature', 'status']
        temperature: bsonType=double, min=-50, max=100
        status: enum=['active', 'inactive', 'maintenance']
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from pymongo.errors import WriteError, OperationFailure

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()

print("\n── Schema Validation ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Define the JSON Schema
# ─────────────────────────────────────────────────────────────────────────────
SENSOR_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Sensor Document",
        "required": ["sensor_id", "location", "temperature", "status"],
        "additionalProperties": True,   # allow extra fields for flexibility
        "properties": {
            "sensor_id": {
                "bsonType": "string",
                "description": "Unique sensor identifier — required, non-empty.",
                "minLength": 1,
            },
            "location": {
                "bsonType": "string",
                "description": "Physical location label — required.",
                "minLength": 1,
            },
            "temperature": {
                "bsonType": "double",
                "description": "Temperature reading in Celsius — required, -50 to 100.",
                "minimum": -50.0,
                "maximum": 100.0,
            },
            "status": {
                "bsonType": "string",
                "enum": ["active", "inactive", "maintenance"],
                "description": "Sensor operational status.",
            },
            "tags": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Optional classification tags.",
            },
            "recorded_at": {
                "bsonType": "date",
                "description": "Timestamp of reading.",
            },
        },
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create collection with the validator attached
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("sensors")
db.create_collection(
    "sensors",
    validator=SENSOR_SCHEMA,
    validationLevel="strict",     # validate ALL inserts and updates
    validationAction="error",     # reject invalid writes
)
sensors = db["sensors"]
print("\n  Created validated 'sensors' collection.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Valid insert — passes all rules
# ─────────────────────────────────────────────────────────────────────────────
try:
    sensors.insert_one({
        "sensor_id":   "sensor-001",
        "location":    "Server Room A",
        "temperature": 22.5,           # double — correct
        "status":      "active",
        "tags":        ["temperature", "datacenter"],
        "recorded_at": datetime.now(tz=timezone.utc),
    })
    print("  [✓] Valid document inserted: sensor-001")
except WriteError as e:
    print(f"  [✗] Unexpected failure: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Missing required field — 'location' absent
# ─────────────────────────────────────────────────────────────────────────────
try:
    sensors.insert_one({
        "sensor_id":   "sensor-002",
        # "location" is missing — required field
        "temperature": 19.1,
        "status":      "active",
    })
    print("  [✗] Should have failed — missing required field!")
except WriteError as e:
    print(f"  [✗] Missing required 'location':\n      {e.details.get('errmsg', str(e))[:60]}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Wrong type — temperature sent as string instead of double
# ─────────────────────────────────────────────────────────────────────────────
try:
    sensors.insert_one({
        "sensor_id":   "sensor-003",
        "location":    "Warehouse B",
        "temperature": "warm",   # string — should be double!
        "status":      "active",
    })
    print("  [✗] Should have failed — wrong type!")
except WriteError as e:
    print(f"  [✗] Invalid type for 'temperature' (string instead of double):\n"
          f"      {e.details.get('errmsg', str(e))[:60]}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Enum violation — status not in allowed list
# ─────────────────────────────────────────────────────────────────────────────
try:
    sensors.insert_one({
        "sensor_id":   "sensor-004",
        "location":    "Lab",
        "temperature": 24.0,
        "status":      "broken",   # not in enum!
    })
    print("  [✗] Should have failed — enum violation!")
except WriteError as e:
    print(f"  [✗] Status out of enum: 'broken' not in enum:\n"
          f"      {e.details.get('errmsg', str(e))[:60]}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. Demonstrate validationLevel="moderate"
#    Moderate: validate inserts strictly, but allow updates to documents that
#    ALREADY fail validation. Useful when migrating schema on a live collection.
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("sensors_moderate")
db.create_collection(
    "sensors_moderate",
    validationLevel="off",          # start without validation so we can insert a bad doc
)
sm = db["sensors_moderate"]
# Insert a doc that does NOT conform (we have validation off)
sm.insert_one({"sensor_id": "bad-doc", "status": "broken", "temperature": "oops"})

# Now switch to moderate — the existing bad doc won't be re-validated on updates
try:
    db.command("collMod", "sensors_moderate",
               validator=SENSOR_SCHEMA,
               validationLevel="moderate",
               validationAction="error")
    # This update touches the pre-existing bad doc — moderate allows it
    sm.update_one({"sensor_id": "bad-doc"}, {"$set": {"note": "legacy"}})
    print("  [✓] Moderate validation — old invalid doc updated without error.")
except OperationFailure as e:
    print(f"  [!] collMod error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Print the validator rules back out from the collection metadata
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Validator rules for 'sensors':")
col_info = db.command("listCollections", filter={"name": "sensors"})
options = col_info["cursor"]["firstBatch"][0].get("options", {})
schema = options.get("validator", {}).get("$jsonSchema", {})
required = schema.get("required", [])
props = schema.get("properties", {})
print(f"    required: {required}")
for field, rules in props.items():
    if "enum" in rules:
        print(f"    {field}: enum={rules['enum']}")
    elif "minimum" in rules or "maximum" in rules:
        print(f"    {field}: bsonType={rules.get('bsonType')}, "
              f"min={rules.get('minimum')}, max={rules.get('maximum')}")

# cleanup
db.drop_collection("sensors_moderate")
print()
