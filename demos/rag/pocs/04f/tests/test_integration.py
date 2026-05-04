import json
import time
import urllib.request


def _get_json(url: str, timeout_seconds: int = 20) -> tuple[int, dict]:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return response.status, payload
        except Exception as exc:  # pragma: no cover - startup timing branch
            last_error = exc
            time.sleep(1)
    raise AssertionError(f"Request did not succeed before timeout: {url} ({last_error})")


def test_health_endpoint_returns_deterministic_ok() -> None:
    status, payload = _get_json("http://127.0.0.1:8000/health")
    assert status == 200
    assert payload == {"ok": True}


def test_ping_endpoint_returns_deterministic_ok() -> None:
    status, payload = _get_json("http://127.0.0.1:8000/ping")
    assert status == 200
    assert payload == {"ok": True}
