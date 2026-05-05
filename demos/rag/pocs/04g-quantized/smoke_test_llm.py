# smoke_test_llm.py
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8002"


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    print("=== 04g LLM Smoke Test ===")

    print("\n[1] Health check")
    health = get_json(f"{BASE_URL}/health")
    print(json.dumps(health, indent=2))

    print("\n[2] Inference check")
    result = post_json(
        f"{BASE_URL}/infer",
        {
            "query": "Explain what an AC repair service does in one short paragraph."
        },
    )
    print(json.dumps(result, indent=2))

    print("\nPASS: LLM container responded successfully.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        print(f"\nFAIL: Could not reach {BASE_URL}. Is llm_7b_run running?")
        print(exc)
        raise SystemExit(1)
    except Exception as exc:
        print("\nFAIL: Smoke test failed.")
        print(exc)
        raise SystemExit(1)