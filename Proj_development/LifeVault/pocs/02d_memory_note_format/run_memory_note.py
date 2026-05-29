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
RAW_OUT = OUT_DIR / "memory_note_raw.txt"
CLEAN_OUT = OUT_DIR / "memory_note_clean.txt"
JSON_OUT = OUT_DIR / "memory_note.json"
REPORT_OUT = OUT_DIR / "memory_note_report.txt"

LABELS = [
    "MEMORY_DESCRIPTION",
    "FUTURE_SEARCHES",
    "TAGS",
    "DATE_HINTS",
    "CONFIDENCE",
]
VALID_CONFIDENCE = {"low", "medium", "high"}


def post_infer(query_text: str):
    payload = {"query": query_text}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(INFER_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def parse_labels(raw_text: str):
    sections = {k: "" for k in LABELS}
    current = None

    for line in raw_text.splitlines():
        stripped = line.strip()
        matched_label = None
        for label in LABELS:
            prefix = label + ":"
            if stripped.upper().startswith(prefix):
                matched_label = label
                value = stripped[len(prefix):].strip()
                sections[label] = value
                current = label
                break
        if matched_label is None and current and stripped:
            if sections[current]:
                sections[current] += " " + stripped
            else:
                sections[current] = stripped

    found = [k for k, v in sections.items() if v.strip()]
    parsing_worked = len(found) > 0
    return sections, found, parsing_worked


def split_phrases(text: str):
    if not text.strip():
        return []
    raw_parts = []
    for chunk in text.replace(";", "\n").split("\n"):
        raw_parts.extend(chunk.split(","))
    cleaned = []
    for p in raw_parts:
        s = p.strip(" -\t")
        if s:
            cleaned.append(s)
    return cleaned


def dedupe_keep_order(items):
    out = []
    seen = set()
    for item in items:
        key = item.lower()
        if key not in seen:
            out.append(item)
            seen.add(key)
    return out


def normalize_token(text: str) -> str:
    t = text.strip()
    low = t.lower()
    if low == "py spark":
        return "PySpark"
    return t


def expand_and_normalize_tags(items):
    out = []
    for raw in items:
        t = normalize_token(raw)
        low = t.lower()

        if low == "financial services":
            out.append("finance")
            continue
        if low == "senior data engineer":
            out.append("data engineer")
            continue
        if low == "sql etl":
            out.append("sql")
            out.append("etl")
            continue

        out.append(t)

    return dedupe_keep_order(out)


def extract_date_hints(memory_description: str, future_searches: list[str]):
    text = memory_description + "\n" + "\n".join(future_searches)

    patterns = [
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
        r"\b\d{4}\b",
    ]

    hits = []
    for pat in patterns:
        hits.extend(re.findall(pat, text, flags=re.IGNORECASE))

    cleaned = [h.strip() for h in hits if h.strip()]
    return dedupe_keep_order(cleaned)


def normalize(parsed_sections: dict):
    memory_description = parsed_sections.get("MEMORY_DESCRIPTION", "").strip()
    future_searches = [normalize_token(x) for x in split_phrases(parsed_sections.get("FUTURE_SEARCHES", ""))]
    future_searches = dedupe_keep_order(future_searches)

    raw_tags = split_phrases(parsed_sections.get("TAGS", ""))
    if not raw_tags:
        raw_tags = future_searches[:]  # derive from future_searches when missing
    tags = expand_and_normalize_tags(raw_tags)
    tags = tags[:10]

    raw_date_hints = split_phrases(parsed_sections.get("DATE_HINTS", ""))
    if not raw_date_hints:
        raw_date_hints = extract_date_hints(memory_description, future_searches)
    date_hints = dedupe_keep_order([normalize_token(x) for x in raw_date_hints])

    original_conf = parsed_sections.get("CONFIDENCE", "").strip().lower()
    if original_conf == "high":
        confidence = "high"
    elif memory_description and future_searches:
        confidence = "medium"
    elif original_conf in VALID_CONFIDENCE:
        confidence = original_conf
    else:
        confidence = "low"

    return {
        "memory_description": memory_description,
        "future_searches": future_searches,
        "tags": tags,
        "date_hints": date_hints,
        "confidence": confidence,
    }


def build_clean_text(note: dict):
    lines = [
        f"MEMORY_DESCRIPTION: {note['memory_description']}",
        f"FUTURE_SEARCHES: {', '.join(note['future_searches'])}",
        f"TAGS: {', '.join(note['tags'])}",
        f"DATE_HINTS: {', '.join(note['date_hints'])}",
        f"CONFIDENCE: {note['confidence']}",
    ]
    return "\n".join(lines) + "\n"


def is_non_empty(note: dict) -> bool:
    return bool(
        note.get("memory_description", "").strip()
        or note.get("future_searches")
        or note.get("tags")
        or note.get("date_hints")
    )


def main():
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    text = INPUT_FILE.read_text(encoding="utf-8")
    prompt = f'''Read the input and produce a label-based memory note using exactly these sections:
MEMORY_DESCRIPTION:
FUTURE_SEARCHES:
TAGS:
DATE_HINTS:
CONFIDENCE:

Rules:
- Do not use JSON.
- Do not use markdown.
- Keep each section short.
- FUTURE_SEARCHES should contain 3 to 7 phrases a human might type later.
- TAGS should be comma-separated.
- DATE_HINTS should be comma-separated.
- CONFIDENCE should be low, medium, or high.

Input:
{text}
'''

    infer_worked = False
    parse_worked = False
    sections_found = []

    try:
        status, body = post_infer(prompt)
        infer_worked = 200 <= status < 300
        if not infer_worked:
            raise RuntimeError(f"HTTP {status}: {body[:1000]}")

        api_obj = json.loads(body)
        answer = str(api_obj.get("answer", "")).strip()
        RAW_OUT.write_text(answer + "\n", encoding="utf-8")

        parsed_sections, sections_found, parse_worked = parse_labels(answer)
        note = normalize(parsed_sections)

    except Exception as e:
        err = f"ERROR: {type(e).__name__}: {e}"
        RAW_OUT.write_text(err + "\n", encoding="utf-8")
        note = normalize({})

    clean_text = build_clean_text(note)
    CLEAN_OUT.write_text(clean_text, encoding="utf-8")
    JSON_OUT.write_text(json.dumps(note, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - start
    non_empty = is_non_empty(note)

    report_lines = [
        f"infer_worked: {infer_worked}",
        f"elapsed_seconds: {elapsed:.2f}",
        f"label_parsing_worked: {parse_worked}",
        f"sections_found: {', '.join(sections_found) if sections_found else '(none)'}",
        f"final_memory_note_non_empty: {non_empty}",
    ]
    REPORT_OUT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n".join(report_lines))
    print(clean_text)


if __name__ == "__main__":
    main()
