import json
import time
import urllib.error
import urllib.request


def _wait_for_service(timeout_seconds: int = 20) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if response.status == 200 and payload == {"ok": True}:
                    return
        except Exception:
            time.sleep(1)
    raise AssertionError("Service did not become ready for validation test")


def test_unknown_endpoint_returns_not_found() -> None:
    _wait_for_service()
    request = urllib.request.Request("http://127.0.0.1:8000/unknown-endpoint")
    try:
        urllib.request.urlopen(request, timeout=5)
        raise AssertionError("Expected 404 for unknown endpoint")
    except urllib.error.HTTPError as exc:
        assert exc.code == 404
