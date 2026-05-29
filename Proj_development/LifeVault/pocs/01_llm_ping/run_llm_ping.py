import json
import time
from pathlib import Path
from urllib import error, request

BASE_URL = "http://localhost:8002"
INFER_URL = BASE_URL + "/infer"
OUTPUT_FILE = Path(__file__).resolve().parent / "outputs" / "llm_ping_response.txt"
PROMPT = "Say OK."
TIMEOUT_SECONDS = 180


def post_infer(query_text: str):
    payload = {"query": query_text}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(INFER_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def main():
    start = time.perf_counter()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        status, body = post_infer(PROMPT)
        elapsed = time.perf_counter() - start

        if not (200 <= status < 300):
            msg = f"Request failed: HTTP {status}\nBody preview: {body[:1000]}\nElapsed seconds: {elapsed:.2f}\n"
            print(msg)
            OUTPUT_FILE.write_text(msg, encoding="utf-8")
            return

        parsed = json.loads(body)
        answer = str(parsed.get("answer", "")).strip()
        if not answer:
            answer = "(empty answer field)"

        OUTPUT_FILE.write_text(answer + "\n", encoding="utf-8")
        print(answer)
        print(f"Elapsed seconds: {elapsed:.2f}")

    except TimeoutError:
        elapsed = time.perf_counter() - start
        msg = (
            "Timeout while calling /infer.\n"
            f"Timeout seconds: {TIMEOUT_SECONDS}\n"
            f"Elapsed seconds: {elapsed:.2f}\n"
        )
        print(msg)
        OUTPUT_FILE.write_text(msg, encoding="utf-8")
    except error.URLError as e:
        elapsed = time.perf_counter() - start
        if isinstance(e.reason, TimeoutError):
            msg = (
                "Timeout while calling /infer.\n"
                f"Timeout seconds: {TIMEOUT_SECONDS}\n"
                f"Elapsed seconds: {elapsed:.2f}\n"
            )
        else:
            msg = f"URLError: {e}\nElapsed seconds: {elapsed:.2f}\n"
        print(msg)
        OUTPUT_FILE.write_text(msg, encoding="utf-8")
    except Exception as e:
        elapsed = time.perf_counter() - start
        msg = f"{type(e).__name__}: {e}\nElapsed seconds: {elapsed:.2f}\n"
        print(msg)
        OUTPUT_FILE.write_text(msg, encoding="utf-8")


if __name__ == "__main__":
    main()
