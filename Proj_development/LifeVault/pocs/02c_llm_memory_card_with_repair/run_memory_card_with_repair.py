import json
import re
import time
from pathlib import Path
from urllib import request

BASE_URL = "http://localhost:8002"
INFER_URL = BASE_URL + "/infer"
TIMEOUT_SECONDS = 240

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_input.txt"
OUT_DIR = BASE_DIR / "outputs"
RAW_OUT = OUT_DIR / "memory_card_raw_response.txt"
CARD_OUT = OUT_DIR / "memory_card.json"
REPORT_OUT = OUT_DIR / "memory_card_report.txt"

VALID_CONFIDENCE = {"low", "medium", "high"}


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
        t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def extract_candidate_json(text: str) -> str:
    s = strip_markdown_fences(text)
    first_obj = s.find("{")
    last_obj = s.rfind("}")
    if first_obj != -1 and last_obj != -1 and last_obj > first_obj:
        return s[first_obj : last_obj + 1].strip()
    first_arr = s.find("[")
    last_arr = s.rfind("]")
    if first_arr != -1 and last_arr != -1 and last_arr > first_arr:
        return s[first_arr : last_arr + 1].strip()
    return s


def as_string(value) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return str(value)


def list_of_strings(value):
    if not isinstance(value, list):
        return []
    cleaned = []
    for item in value:
        if isinstance(item, str):
            s = item.strip()
            if s:
                cleaned.append(s)
        elif item is not None:
            s = str(item).strip()
            if s:
                cleaned.append(s)
    return cleaned


def normalize(obj: dict):
    title = as_string(obj.get("title", "")).strip()
    item_type_guess = as_string(obj.get("item_type_guess", "")).strip()
    dates = list_of_strings(obj.get("dates", []))
    tags = list_of_strings(obj.get("tags", []))[:6]
    confidence = as_string(obj.get("confidence", "")).strip().lower()
    if confidence not in VALID_CONFIDENCE:
        confidence = "low"
    return {
        "title": title,
        "item_type_guess": item_type_guess,
        "dates": dates,
        "tags": tags,
        "confidence": confidence,
    }


def is_valid_card(card: dict) -> bool:
    if not isinstance(card, dict):
        return False
    if sorted(card.keys()) != sorted(["title", "item_type_guess", "dates", "tags", "confidence"]):
        return False
    if not isinstance(card["title"], str):
        return False
    if not isinstance(card["item_type_guess"], str):
        return False
    if not isinstance(card["dates"], list) or not all(isinstance(x, str) for x in card["dates"]):
        return False
    if not isinstance(card["tags"], list) or not all(isinstance(x, str) for x in card["tags"]):
        return False
    if len(card["tags"]) > 6:
        return False
    if card["confidence"] not in VALID_CONFIDENCE:
        return False
    return True


def is_non_empty_card(card: dict) -> bool:
    return bool(
        card.get("title", "").strip()
        or card.get("item_type_guess", "").strip()
        or card.get("dates")
        or card.get("tags")
    )


def salvage_fields(raw_text: str):
    s = strip_markdown_fences(raw_text)
    partial = {}
    salvaged_fields = []

    m_title = re.search(r'"title"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', s)
    if m_title:
        partial["title"] = m_title.group(1)
        salvaged_fields.append("title")

    m_item = re.search(r'"item_type_guess"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', s)
    if m_item:
        partial["item_type_guess"] = m_item.group(1)
        salvaged_fields.append("item_type_guess")

    m_conf = re.search(r'"confidence"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', s)
    if m_conf:
        partial["confidence"] = m_conf.group(1)
        salvaged_fields.append("confidence")

    m_dates = re.search(r'"dates"\s*:\s*\[(.*?)\]', s, flags=re.DOTALL)
    if m_dates:
        dates_block = m_dates.group(1)
        dates = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', dates_block)
        partial["dates"] = dates
        salvaged_fields.append("dates")

    m_tags = re.search(r'"tags"\s*:\s*\[(.*)', s, flags=re.DOTALL)
    if m_tags:
        tags_block = m_tags.group(1)
        tags = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', tags_block)
        if tags:
            partial["tags"] = tags[:6]
            salvaged_fields.append("tags")

    return partial, salvaged_fields


def main():
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_text = INPUT_FILE.read_text(encoding="utf-8")
    prompt = f'''Return one JSON object only.
No markdown.
No explanation.
No code fence.
Keep string values short.
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

    infer_worked = False
    direct_parse_worked = False
    repair_parse_worked = False
    salvage_used = False
    salvaged_fields = []
    final_valid = False
    final_non_empty = False
    answer_text = ""

    try:
        status, body = post_infer(prompt)
        infer_worked = 200 <= status < 300
        if not infer_worked:
            raise RuntimeError(f"HTTP {status}: {body[:1000]}")

        api_obj = json.loads(body)
        answer_text = as_string(api_obj.get("answer", "")).strip()
        RAW_OUT.write_text(answer_text + "\n", encoding="utf-8")

        parsed_obj = None
        try:
            parsed_candidate = json.loads(answer_text)
            direct_parse_worked = True
            if isinstance(parsed_candidate, list):
                parsed_obj = parsed_candidate[0] if parsed_candidate and isinstance(parsed_candidate[0], dict) else {}
            elif isinstance(parsed_candidate, dict):
                parsed_obj = parsed_candidate
            else:
                parsed_obj = {}
        except Exception:
            try:
                candidate_text = extract_candidate_json(answer_text)
                parsed_candidate = json.loads(candidate_text)
                repair_parse_worked = True
                if isinstance(parsed_candidate, list):
                    parsed_obj = parsed_candidate[0] if parsed_candidate and isinstance(parsed_candidate[0], dict) else {}
                elif isinstance(parsed_candidate, dict):
                    parsed_obj = parsed_candidate
                else:
                    parsed_obj = {}
            except Exception:
                salvage_used = True
                partial, salvaged_fields = salvage_fields(answer_text)
                parsed_obj = partial

        repaired = normalize(parsed_obj)
        final_valid = is_valid_card(repaired)
        final_non_empty = is_non_empty_card(repaired)
        CARD_OUT.write_text(json.dumps(repaired, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    except Exception as e:
        answer_text = f"ERROR: {type(e).__name__}: {e}"
        RAW_OUT.write_text(answer_text + "\n", encoding="utf-8")
        repaired = normalize({})
        final_valid = is_valid_card(repaired)
        final_non_empty = is_non_empty_card(repaired)
        CARD_OUT.write_text(json.dumps(repaired, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - start

    report_lines = [
        f"infer_worked: {infer_worked}",
        f"elapsed_seconds: {elapsed:.2f}",
        f"direct_json_parse_worked: {direct_parse_worked}",
        f"repair_parse_worked: {repair_parse_worked}",
        f"salvage_used: {salvage_used}",
        f"salvaged_fields: {', '.join(salvaged_fields) if salvaged_fields else '(none)'}",
        f"final_memory_card_valid: {final_valid}",
        f"final_memory_card_non_empty: {final_non_empty}",
    ]
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n".join(report_lines))
    print(json.dumps(repaired, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
