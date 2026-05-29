import json
from pathlib import Path
from urllib import error, request

BASE_URL = "http://localhost:8002"
TIMEOUT_SECONDS = 30
MAX_BODY_CHARS = 1000

GET_ROUTES = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/routes",
    "/api",
    "/api/tags",
    "/models",
    "/v1/models",
]

POST_ROUTES = [
    "/generate",
    "/predict",
    "/infer",
    "/inference",
    "/completion",
    "/completions",
    "/chat",
    "/chat/completions",
    "/api/generate",
    "/api/chat",
    "/v1/completions",
    "/v1/chat/completions",
]

POST_PAYLOADS = [
    {"prompt": "Say LifeVault API discovery works."},
    {"text": "Say LifeVault API discovery works."},
    {"inputs": "Say LifeVault API discovery works."},
    {
        "messages": [
            {"role": "user", "content": "Say LifeVault API discovery works."}
        ]
    },
]

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "outputs"
RESULTS_JSON = OUT_DIR / "api_discovery_results.json"
SUMMARY_TXT = OUT_DIR / "api_discovery_summary.txt"
OPENAPI_JSON = OUT_DIR / "openapi.json"


def make_result(method: str, url: str, status, content_type: str, body: str, payload=None):
    looks_successful = bool(status and 200 <= status < 300)
    return {
        "method": method,
        "url": url,
        "payload": payload,
        "status_code": status,
        "content_type": content_type,
        "response_body_preview": body[:MAX_BODY_CHARS],
        "looks_successful": looks_successful,
    }


def do_get(url: str):
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            ct = resp.headers.get("Content-Type", "")
            return resp.status, ct, body
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        ct = e.headers.get("Content-Type", "") if e.headers else ""
        return e.code, ct, body
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def do_post(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            ct = resp.headers.get("Content-Type", "")
            return resp.status, ct, body
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        ct = e.headers.get("Content-Type", "") if e.headers else ""
        return e.code, ct, body
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for route in GET_ROUTES:
        url = BASE_URL + route
        status, ct, body = do_get(url)
        results.append(make_result("GET", url, status, ct, body))

        if route == "/openapi.json" and status and 200 <= status < 300:
            OPENAPI_JSON.write_text(body, encoding="utf-8")

    for route in POST_ROUTES:
        url = BASE_URL + route
        for payload in POST_PAYLOADS:
            status, ct, body = do_post(url, payload)
            results.append(make_result("POST", url, status, ct, body, payload=payload))

    RESULTS_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    non_404 = [r for r in results if r["status_code"] != 404]
    successful = [r for r in results if r["looks_successful"]]

    likely_inference = None
    for r in successful:
        if r["method"] == "POST":
            likely_inference = r
            break

    lines = []
    lines.append("LLM API Discovery Summary")
    lines.append("=" * 70)
    lines.append(f"Base URL: {BASE_URL}")
    lines.append(f"Total requests: {len(results)}")
    lines.append(f"Non-404 responses: {len(non_404)}")
    lines.append(f"Successful (2xx): {len(successful)}")
    lines.append("-")

    lines.append("Non-404 routes:")
    if non_404:
        for r in non_404:
            lines.append(f"- {r['method']} {r['url']} -> {r['status_code']} [{r['content_type']}]")
    else:
        lines.append("- none")

    lines.append("-")
    if likely_inference:
        lines.append("Likely inference route found:")
        lines.append(f"- {likely_inference['method']} {likely_inference['url']} (status {likely_inference['status_code']})")
    else:
        lines.append("Likely inference route found:")
        lines.append("- none discovered from tested routes/payloads")

    if OPENAPI_JSON.exists():
        lines.append("-")
        lines.append(f"OpenAPI schema saved: {OPENAPI_JSON}")

    summary = "\n".join(lines) + "\n"
    SUMMARY_TXT.write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
