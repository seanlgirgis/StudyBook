from __future__ import annotations

import argparse
import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from _env_loader import first_non_empty, load_env_file

DEFAULT_ENV_FILE = r"D:\StudyBook\_infra\env\.env.local"

SERVICE_CONFIGS: dict[str, dict[str, Any]] = {
    "postgres": {
        "checks": [
            {"type": "tcp", "env_port_key": "POSTGRES_PORT", "port": 5432},
            {
                "type": "docker_exec",
                "container": "de_postgres",
                "command": ["pg_isready", "-U", "{POSTGRES_USER|de_admin}"],
            },
        ]
    },
    "redis": {
        "checks": [
            {"type": "tcp", "env_port_key": "REDIS_PORT", "port": 6380},
            {
                "type": "docker_exec",
                "container": "de_redis",
                "command": ["redis-cli", "-a", "{REDIS_PASSWORD|change_me}", "PING"],
            },
        ]
    },
    "cassandra": {
        "checks": [
            {"type": "tcp", "env_port_key": "CASSANDRA_PORT", "port": 9042},
            {
                "type": "docker_exec",
                "container": "de_cassandra",
                "command": ["cqlsh", "-e", "DESCRIBE KEYSPACES"],
            },
        ]
    },
    "neo4j": {
        "checks": [
            {"type": "tcp", "env_port_key": "NEO4J_BOLT_PORT", "port": 7687},
            {
                "type": "http",
                "env_port_key": "NEO4J_HTTP_PORT",
                "port": 7474,
                "path": "/",
                "accepted": [200, 301, 302, 401],
            },
        ]
    },
    "influxdb": {
        "checks": [
            {"type": "tcp", "env_port_key": "INFLUXDB_PORT", "port": 8086},
            {
                "type": "http",
                "env_port_key": "INFLUXDB_PORT",
                "port": 8086,
                "path": "/health",
                "accepted": [200, 204],
            },
        ]
    },
    "zookeeper": {
        "checks": [
            {"type": "tcp", "env_port_key": "ZOOKEEPER_PORT", "port": 2181},
            {
                "type": "docker_exec",
                "container": "citi_zookeeper",
                "command": ["bash", "-lc", "cub zk-ready localhost:2181 10"],
            },
        ]
    },
    "kafka": {
        "checks": [
            {"type": "tcp", "env_port_key": "KAFKA_PORT", "port": 9092},
            {
                "type": "docker_exec",
                "container": "citi_kafka",
                "command": ["bash", "-lc", "kafka-topics --bootstrap-server localhost:9092 --list"],
            },
        ]
    },
    "kafka_ui": {
        "checks": [
            {
                "type": "http",
                "env_port_key": "KAFKA_UI_PORT",
                "port": 8080,
                "path": "/",
                "accepted": [200, 301, 302],
            }
        ]
    },
    "spark_master": {
        "checks": [
            {
                "type": "http",
                "env_port_key": "SPARK_MASTER_UI_PORT",
                "port": 8081,
                "path": "/",
                "accepted": [200, 301, 302],
            }
        ]
    },
    "spark_worker": {
        "checks": [
            {
                "type": "http",
                "env_port_key": "SPARK_WORKER_UI_PORT",
                "port": 8085,
                "path": "/",
                "accepted": [200, 301, 302],
            }
        ]
    },
    "airflow": {
        "checks": [
            {"type": "tcp", "env_port_key": "AIRFLOW_PORT", "port": 8082},
            {
                "type": "docker_exec",
                "container": "citi_airflow",
                "command": ["bash", "-lc", "airflow dags list --output table | head -n 20"],
            },
        ]
    },
    "mlflow": {
        "checks": [
            {
                "type": "http",
                "env_port_key": "MLFLOW_PORT",
                "port": 5000,
                "path": "/",
                "accepted": [200, 301, 302],
            }
        ]
    },
    "jupyterlab": {
        "checks": [
            {"type": "tcp", "env_port_key": "JUPYTER_PORT", "port": 8888},
            {
                "type": "http",
                "env_port_key": "JUPYTER_PORT",
                "port": 8888,
                "path": "/lab",
                "accepted": [200, 302, 403],
            },
            {
                "type": "http",
                "env_port_key": "JUPYTER_PORT",
                "port": 8888,
                "path": "/api/status",
                "accepted": [200],
            }
        ]
    },
    "elasticsearch": {
        "checks": [
            {"type": "tcp", "env_port_key": "ELASTIC_PORT", "port": 9200},
            {
                "type": "docker_exec",
                "container": "de_elasticsearch",
                "command": [
                    "bash",
                    "-lc",
                    "curl -s -u elastic:{ELASTIC_PASSWORD|change_me} http://localhost:9200/_cluster/health",
                ],
            },
        ]
    },
    "kibana": {
        "checks": [
            {
                "type": "http",
                "env_port_key": "KIBANA_PORT",
                "port": 5601,
                "path": "/api/status",
                "accepted": [200],
            }
        ]
    },
    "splunk": {
        "checks": [
            {"type": "tcp", "env_port_key": "SPLUNK_PORT_MGT", "port": 8089},
            {
                "type": "docker_exec",
                "container": "citi_splunk",
                "command": [
                    "bash",
                    "-lc",
                    "curl -sk https://localhost:8089/services/server/info -u admin:{SPLUNK_PASSWORD|change_me}",
                ],
            },
        ]
    },
}


def resolve_env_value(env_map: dict[str, str], key: str, fallback: str) -> str:
    value = first_non_empty(env_map.get(key), fallback)
    return value if value is not None else fallback


def resolve_env_port(env_map: dict[str, str], key: str, fallback: int) -> int:
    raw = env_map.get(key)
    if raw:
        try:
            return int(raw)
        except ValueError:
            return fallback
    return fallback


def apply_tokens(text: str, env_map: dict[str, str]) -> str:
    out = text
    while True:
        start = out.find("{")
        if start < 0:
            break
        end = out.find("}", start + 1)
        if end < 0:
            break
        token = out[start + 1 : end]
        if "|" in token:
            key, fallback = token.split("|", 1)
        else:
            key, fallback = token, ""
        replacement = resolve_env_value(env_map, key, fallback)
        out = out[:start] + replacement + out[end + 1 :]
    return out


def tcp_check(name: str, host: str, port: int, timeout_sec: int) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=max(timeout_sec, 1)):
            ok = True
            detail = "TCP connection succeeded."
    except Exception as exc:  # noqa: BLE001
        ok = False
        detail = str(exc)

    return {
        "name": name,
        "method": "tcp",
        "target": f"{host}:{port}",
        "ok": ok,
        "latency_ms": int((time.perf_counter() - start) * 1000),
        "detail": detail,
    }


def http_check(name: str, host: str, port: int, path: str, accepted: list[int], timeout_sec: int) -> dict[str, Any]:
    start = time.perf_counter()
    url = f"http://{host}:{port}{path}"

    code: int | None = None
    detail = ""

    try:
        import requests

        response = requests.get(url, timeout=max(timeout_sec, 1))
        code = int(response.status_code)
        detail = f"HTTP status {code}."
    except ImportError:
        try:
            from urllib import request

            with request.urlopen(url, timeout=max(timeout_sec, 1)) as response:  # nosec B310
                code = int(response.getcode())
            detail = f"HTTP status {code} (urllib fallback)."
        except Exception as exc:  # noqa: BLE001
            code = None
            detail = str(exc)
    except Exception as exc:  # noqa: BLE001
        code = None
        detail = str(exc)

    ok = (code in accepted) if code is not None else False

    return {
        "name": name,
        "method": "http",
        "target": url,
        "ok": ok,
        "latency_ms": int((time.perf_counter() - start) * 1000),
        "detail": detail,
    }


def docker_exec_check(name: str, container: str, command: list[str], timeout_sec: int) -> dict[str, Any]:
    start = time.perf_counter()

    if shutil.which("docker") is None:
        return {
            "name": name,
            "method": "docker_exec",
            "target": f"container:{container}",
            "ok": False,
            "latency_ms": int((time.perf_counter() - start) * 1000),
            "detail": "docker CLI not found.",
        }

    try:
        completed = subprocess.run(
            ["docker", "exec", container, *command],
            capture_output=True,
            text=True,
            timeout=max(timeout_sec, 1),
            check=False,
        )
        output = (completed.stdout or completed.stderr or "").strip()
        if not output:
            output = "docker exec completed."
        if len(output) > 400:
            output = output[:400] + "..."
        ok = completed.returncode == 0
        detail = output
    except Exception as exc:  # noqa: BLE001
        ok = False
        detail = str(exc)

    return {
        "name": name,
        "method": "docker_exec",
        "target": f"container:{container}",
        "ok": ok,
        "latency_ms": int((time.perf_counter() - start) * 1000),
        "detail": detail,
    }


def run_service(service_key: str) -> int:
    parser = argparse.ArgumentParser(description=f"Read-only Docker proof for service '{service_key}'.")
    parser.add_argument("--target-host", default="localhost")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE)
    parser.add_argument("--timeout-sec", type=int, default=12)
    args = parser.parse_args()

    cfg = SERVICE_CONFIGS[service_key]
    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    checks: list[dict[str, Any]] = []
    for idx, check_cfg in enumerate(cfg["checks"], start=1):
        ctype = check_cfg["type"]
        name = f"{service_key}-{idx}"

        if ctype == "tcp":
            port = resolve_env_port(env_map, check_cfg["env_port_key"], int(check_cfg["port"]))
            checks.append(tcp_check(name, args.target_host, port, args.timeout_sec))
            continue

        if ctype == "http":
            port = resolve_env_port(env_map, check_cfg["env_port_key"], int(check_cfg["port"]))
            path = str(check_cfg.get("path", "/"))
            accepted = [int(x) for x in check_cfg.get("accepted", [200])]
            checks.append(http_check(name, args.target_host, port, path, accepted, args.timeout_sec))
            continue

        if ctype == "docker_exec":
            container = str(check_cfg["container"])
            cmd = [apply_tokens(str(part), env_map) for part in check_cfg["command"]]
            checks.append(docker_exec_check(name, container, cmd, args.timeout_sec))
            continue

        checks.append(
            {
                "name": name,
                "method": ctype,
                "target": "n/a",
                "ok": False,
                "latency_ms": 0,
                "detail": f"Unsupported check type: {ctype}",
            }
        )

    ok = all(bool(c.get("ok")) for c in checks)
    result = {
        "ok": ok,
        "proof": "docker_service_read_only",
        "service": service_key,
        "env_file_checked": str(env_file),
        "checks": checks,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if ok else 1


def main_for_service(service_key: str) -> int:
    if service_key not in SERVICE_CONFIGS:
        print(json.dumps({"ok": False, "error": f"Unknown service key: {service_key}"}, indent=2))
        return 2
    return run_service(service_key)



