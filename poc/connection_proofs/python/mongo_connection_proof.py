from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
from pathlib import Path

import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from _env_loader import first_non_empty, load_env_file

try:
    import certifi
except Exception:  # noqa: BLE001
    certifi = None


def build_connection_uri(env_map: dict[str, str], cli_uri: str | None) -> str | None:
    uri = first_non_empty(cli_uri, os.getenv("MONGODB_URI"), env_map.get("MONGODB_URI"))
    if uri:
        return uri

    host = first_non_empty(os.getenv("MONGODB_HOST"), env_map.get("MONGODB_HOST"))
    user = first_non_empty(os.getenv("MONGODB_USER"), env_map.get("MONGODB_USER"))
    password = first_non_empty(os.getenv("MONGODB_PASSWORD"), env_map.get("MONGODB_PASSWORD"))
    database = first_non_empty(os.getenv("MONGODB_DATABASE"), env_map.get("MONGODB_DATABASE"), "admin")

    if not host:
        return None

    if host.startswith("mongodb://") or host.startswith("mongodb+srv://"):
        return host

    if user and password:
        if ":" in host:
            return f"mongodb://{user}:{password}@{host}/{database}"
        return f"mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true&w=majority"

    if ":" in host:
        return f"mongodb://{host}/{database}"

    return f"mongodb+srv://{host}/{database}?retryWrites=true&w=majority"


def build_client_options(uri: str, args: argparse.Namespace) -> dict[str, object]:
    options: dict[str, object] = {
        "serverSelectionTimeoutMS": args.timeout_ms,
    }

    # Atlas / SRV endpoints require TLS. Force explicit TLS so behavior is clear.
    needs_tls = uri.startswith("mongodb+srv://") or ".mongodb.net" in uri
    if needs_tls:
        options["tls"] = True

    if args.tls_ca_file:
        options["tlsCAFile"] = args.tls_ca_file
    elif needs_tls and certifi is not None:
        options["tlsCAFile"] = certifi.where()

    if args.insecure_skip_tls_verify:
        options["tlsAllowInvalidCertificates"] = True

    return options


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only MongoDB connection proof.")
    parser.add_argument("--uri", help="MongoDB URI override.")
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to local env file with MONGODB_* variables.",
    )
    parser.add_argument("--timeout-ms", type=int, default=5000, help="Connection timeout in milliseconds.")
    parser.add_argument("--max-dbs", type=int, default=5, help="How many database names to show.")
    parser.add_argument("--tls-ca-file", help="Path to CA bundle PEM file (optional).")
    parser.add_argument(
        "--insecure-skip-tls-verify",
        action="store_true",
        help="Troubleshooting only: skip TLS cert verification.",
    )
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)
    uri = build_connection_uri(env_map, args.uri)

    diagnostics: dict[str, object] = {
        "python_version": sys.version,
        "openssl_version": ssl.OPENSSL_VERSION,
        "pymongo_version": pymongo.version,
        "certifi_available": certifi is not None,
        "certifi_path": certifi.where() if certifi is not None else None,
    }

    if not uri:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "Missing MongoDB connection details. Provide --uri or MONGODB_URI.",
                    "env_file_checked": str(env_file),
                    "diagnostics": diagnostics,
                },
                indent=2,
            )
        )
        return 2

    client_options = build_client_options(uri, args)

    start = time.perf_counter()
    result: dict[str, object] = {
        "ok": False,
        "proof": "mongodb_read_only",
        "env_file_checked": str(env_file),
        "diagnostics": diagnostics,
        "client_options": {
            "serverSelectionTimeoutMS": client_options.get("serverSelectionTimeoutMS"),
            "tls": client_options.get("tls", False),
            "tlsCAFile_set": bool(client_options.get("tlsCAFile")),
            "tlsAllowInvalidCertificates": bool(client_options.get("tlsAllowInvalidCertificates", False)),
        },
    }

    try:
        client = MongoClient(uri, **client_options)
        ping_response = client.admin.command("ping")
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        dbs = client.list_database_names()

        result.update(
            {
                "ok": True,
                "latency_ms": elapsed_ms,
                "ping": ping_response,
                "database_count": len(dbs),
                "database_sample": dbs[: max(args.max_dbs, 0)],
            }
        )
        print(json.dumps(result, indent=2, default=str))
        return 0
    except PyMongoError as exc:
        result["error"] = str(exc)
        print(json.dumps(result, indent=2, default=str))
        return 1


if __name__ == "__main__":
    sys.exit(main())
