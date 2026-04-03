"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisite Check                                           ║
║  Verify your environment before running any other nugget.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Checks everything you need is in place:
  1. Python version (≥ 3.9)
  2. Required packages installed (pymongo, certifi)
  3. Credentials resolved (URI or host+user+password)
  4. Live connection test (ping Atlas cluster)

WHY THIS MATTERS
────────────────
MongoDB Atlas uses a completely different connection model than traditional SQL:
  - No JDBC/ODBC driver — pymongo is the native Python driver.
  - Authentication is via username + password embedded in the URI, or
    SCRAM-SHA-256 (default for Atlas), x.509 certificates, or AWS IAM.
  - The URI is the entire connection configuration: host, auth, TLS, options.
  - TLS is mandatory on Atlas — all traffic is encrypted in transit.

pymongo vs motor:
  - pymongo   — synchronous driver (this is what all nuggets use).
  - motor     — async driver wrapping pymongo for asyncio / Tornado apps.
  - For data engineering scripts (not web servers), pymongo is standard.

CREDENTIAL RESOLUTION ORDER
────────────────────────────
  1. Environment variables  MONGODB_URI, MONGODB_HOST, MONGODB_USER, ...
     → Set by env_setter.ps1 from encrypted secrets
  2. Encrypted secrets file  config/secrets/asuspc.secrets.enc.json
     → Decrypted via StudyBook seed-backed DPAPI system
  3. .env.local file  _infra/env/.env.local
     → Local override (gitignored)

USAGE
─────
    python 00_prereq_check.py

EXPECTED OUTPUT
───────────────
    ── MongoDB Prerequisite Check ──────────────────────

      [✓] Python 3.12.9
      [✓] pymongo 4.16.0
      [✓] certifi 2025.x.x  (CA bundle: C:\\...\\cacert.pem)

      Credentials resolved:
        URI:     mongodb+srv://de_admin:***@de-learning.zur1dze.mongodb.net/...
        Source:  env_file

      Testing live connection...
      [✓] Connected to Atlas!
        Cluster:   de-learning.zur1dze.mongodb.net
        Round-trip latency: ~1030 ms
        Databases visible: ['de_telemetry', 'sample_mflix', 'admin', 'local']

      All prerequisites met. Ready to run nuggets!
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_creds, get_client, _build_uri, _ENV_FILE

print("\n── MongoDB Prerequisite Check ──────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python version check
#    pymongo 4.x requires Python ≥ 3.7; pymongo 4.9+ requires ≥ 3.9.
#    The async motor driver requires ≥ 3.9 as well.
# ─────────────────────────────────────────────────────────────────────────────
py_ok = sys.version_info >= (3, 9)
status = "✓" if py_ok else "✗"
print(f"\n  [{status}] Python {sys.version.split()[0]}  (requires ≥ 3.9)")
if not py_ok:
    print("  Fix: upgrade Python to 3.9 or newer.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Package checks
#    pymongo — the official MongoDB Python driver.
#      - Implements the MongoDB wire protocol natively (not ODBC/JDBC).
#      - Provides MongoClient, collection operations, aggregation, change streams.
#      - Thread-safe; one MongoClient per process is the recommended pattern.
#      - Version 4.x is the current stable series (major refactor from 3.x).
#
#    certifi — Mozilla's CA certificate bundle.
#      - Provides a curated set of Root CA certificates for TLS validation.
#      - Required because Atlas uses TLS and Python's ssl module needs a CA file
#        on Windows where the system trust store is not always used.
#      - certifi.where() returns the path to the cacert.pem file.
# ─────────────────────────────────────────────────────────────────────────────
for pkg_name, import_name in [
    ("pymongo", "pymongo"),
    ("certifi", "certifi"),
]:
    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "unknown")
        extra = ""
        if import_name == "certifi":
            extra = f"  (CA bundle: {mod.where()})"
        print(f"  [✓] {pkg_name} {version}{extra}")
    except ImportError:
        print(f"  [✗] {pkg_name} — NOT INSTALLED")
        print(f"      Fix: pip install {pkg_name}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Credential check
#    MongoDB Atlas needs ONE of these:
#      MONGODB_URI — the full connection string (easiest)
#        Format: mongodb+srv://user:pass@cluster.mongodb.net/db?options
#        The "mongodb+srv://" scheme uses DNS SRV records to discover nodes.
#        This means you never hard-code specific replica set member IPs.
#
#      OR: MONGODB_HOST + MONGODB_USER + MONGODB_PASSWORD
#        The helper builds the URI from these components.
#
#    Optional: MONGODB_DATABASE
#        The database name embedded in the URI (used for auth source).
#        Defaults to "admin" if not specified.
# ─────────────────────────────────────────────────────────────────────────────
creds = get_creds()

# Mask the password in the displayed URI
uri_raw = creds.get("MONGODB_URI") or ""
password = creds.get("MONGODB_PASSWORD") or ""
uri_display = uri_raw
if password and password in uri_raw:
    uri_display = uri_raw.replace(password, "***")
elif uri_raw:
    # Already has *** or no password in URI
    uri_display = uri_raw[:60] + "..." if len(uri_raw) > 60 else uri_raw

# Determine source
source = "unknown"
if os.getenv("MONGODB_URI") or os.getenv("MONGODB_HOST"):
    source = "environment_variables"
elif uri_raw:
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    enc_file = project_root / "config" / "secrets" / "asuspc.secrets.enc.json"
    source = "encrypted_secrets" if enc_file.exists() else "env_file"

print("\n  Credentials resolved:")
print(f"    URI:     {uri_display or 'MISSING'}")
print(f"    Source:  {source}")

if not (creds.get("MONGODB_URI") or creds.get("MONGODB_HOST")):
    print("\n  [✗] Missing credentials!")
    print("  Fix options:")
    print("    1. Add MONGODB_URI to your encrypted secrets:")
    print("       .\\scripts\\env\\set_secret.ps1 -Machine asuspc -PromptSecretKey MONGODB_URI")
    print(f"    2. Add to {_ENV_FILE}:")
    print("       MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Live connection test
#    We use the "ping" admin command — the lightest possible server probe.
#    It returns {"ok": 1} if the cluster is reachable and the credentials work.
#
#    Atlas cold-connect latency:
#      First connection involves: DNS SRV lookup → TCP → TLS handshake → SCRAM auth
#      This typically takes 800 ms–2 s on a cold start (subsequent calls: < 50 ms).
#
#    serverSelectionTimeoutMS:
#      If the driver cannot find a suitable server within this window,
#      it raises ServerSelectionTimeoutError. We use 8 s to accommodate
#      slow DNS or network hops on first connect.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Testing live connection...")
try:
    t0 = time.perf_counter()
    client = get_client()
    ping = client.admin.command("ping")
    latency_ms = int((time.perf_counter() - t0) * 1000)
    dbs = client.list_database_names()
    client.close()

    print(f"  [✓] Connected to Atlas!")
    # Extract cluster hostname from URI
    uri_built = _build_uri(creds)
    cluster = uri_built.split("@")[-1].split("/")[0] if "@" in uri_built else "unknown"
    print(f"    Cluster:  {cluster}")
    print(f"    Latency:  ~{latency_ms} ms (cold connect including TLS + SCRAM)")
    print(f"    Databases visible: {dbs}")
    print(f"\n  All prerequisites met. Ready to run nuggets!")

except Exception as exc:
    print(f"  [✗] Connection failed: {exc}")
    print("\n  Common causes:")
    print("    - Invalid URI or wrong password")
    print("    - Your IP is not whitelisted in Atlas Network Access")
    print("    - Firewall blocking port 27017 or 443 (SRV uses 443 for DNS)")
    sys.exit(1)

print()
