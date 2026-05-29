import json
import re
import time
from pathlib import Path
from urllib import error, request

BASE_URL = "http://localhost:8002"
INFER_URL = BASE_URL + "/infer"
TIMEOUT_SECONDS = 240

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_input.txt"
RAW_OUT = BASE_DIR / "outputs" / "memory_card_raw_response.txt"
JSON_OUT = BASE_DIR / "outputs" / "memory_card.json"
ERR_OUT = BASE_DIR / "outputs" / "memory_card_parse_error.txt"


def post_infer(query_text: str):
    payload = {"query": query_text}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(INFER_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def strip_markdown_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z0-9_-]*\\s*", "", t)
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def extract_candidate_json(text: str) -> str:
    s = strip_markdown_fences(text)
    first = s.find("{")
    last = s.rfind("}")
    if first != -1 and last != -1 and last > first:
        return s[first : last + 1].strip()
    return s


def main():
    start = time.perf_counter()
    source_text = INPUT_FILE.read_text(encoding="utf-8")

    prompt = f'''Return one JSON object only.
No markdown.
No explanation.
No code fence.
Keep all string values short.
Maximum 6 tags.
confidence must be low, medium, or high.

Use this schema exactly:
{{
  "title": "",
  "item_type_guess": "",
  "dates": [],
  "tags": [],
  "confidence": ""
}}

Input text:
{source_text}
'''

    RAW_OUT.parent.mkdir(parents=True, exist_ok=True)

    try:
        status, body = post_infer(prompt)
        elapsed = time.perf_counter() - start
        if not (200 <= status < 300):
            err = f"Request failed: HTTP {status}\nBody preview: {body[:1000]}\nElapsed seconds: {elapsed:.2f}\n"
            RAW_OUT.write_text(err, encoding="utf-8")
            ERR_OUT.write_text(err, encoding="utf-8")
            print(err)
            return

        parsed_api = json.loads(body)
        answer_text = str(parsed_api.get("answer", "")).strip()
        RAW_OUT.write_text(answer_text + "\n", encoding="utf-8")

        candidate = extract_candidate_json(answer_text)
        try:
            parsed_card = json.loads(candidate)
            JSON_OUT.write_text(json.dumps(parsed_card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"JSON parsing succeeded. Wrote: {JSON_OUT}")
            print(f"Elapsed seconds: {elapsed:.2f}")
        except Exception as e:
            err_text = (
                "JSON parsing failed.\n"
                f"Error: {type(e).__name__}: {e}\n"
                f"Elapsed seconds: {elapsed:.2f}\n\n"
                "Extracted candidate JSON:\n"
                f"{candidate}\n"
            )
            ERR_OUT.write_text(err_text, encoding="utf-8")
            print(err_text)

    except TimeoutError:
        elapsed = time.perf_counter() - start
        err = (
            "Timeout while calling /infer.\n"
            f"Timeout seconds: {TIMEOUT_SECONDS}\n"
            f"Elapsed seconds: {elapsed:.2f}\n"
        )
        RAW_OUT.write_text(err, encoding="utf-8")
        ERR_OUT.write_text(err, encoding="utf-8")
        print(err)
    except error.URLError as e:
        elapsed = time.perf_counter() - start
        if isinstance(e.reason, TimeoutError):
            err = (
                "Timeout while calling /infer.\n"
                f"Timeout seconds: {TIMEOUT_SECONDS}\n"
                f"Elapsed seconds: {elapsed:.2f}\n"
            )
        else:
            err = f"URLError: {e}\nElapsed seconds: {elapsed:.2f}\n"
        RAW_OUT.write_text(err, encoding="utf-8")
        ERR_OUT.write_text(err, encoding="utf-8")
        print(err)
    except Exception as e:
        elapsed = time.perf_counter() - start
        err = f"{type(e).__name__}: {e}\nElapsed seconds: {elapsed:.2f}\n"
        RAW_OUT.write_text(err, encoding="utf-8")
        ERR_OUT.write_text(err, encoding="utf-8")
        print(err)


if __name__ == "__main__":
    main()
