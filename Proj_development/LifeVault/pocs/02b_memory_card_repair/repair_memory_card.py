import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_bad_llm_output.txt"
OUT_JSON = BASE_DIR / "outputs" / "repaired_memory_card.json"
OUT_REPORT = BASE_DIR / "outputs" / "repair_report.txt"

VALID_CONFIDENCE = {"low", "medium", "high"}


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


def main():
    raw = INPUT_FILE.read_text(encoding="utf-8")

    notes = []
    repair_succeeded = False

    try:
        parsed = json.loads(raw)
        notes.append("JSON parse: success")

        if isinstance(parsed, list):
            notes.append("Top-level type: list -> using first object")
            if parsed and isinstance(parsed[0], dict):
                candidate = parsed[0]
            else:
                notes.append("First list item is not an object; using empty object")
                candidate = {}
        elif isinstance(parsed, dict):
            notes.append("Top-level type: object")
            candidate = parsed
        else:
            notes.append(f"Top-level type: {type(parsed).__name__} -> using empty object")
            candidate = {}

        repaired = normalize(candidate)
        repair_succeeded = True

    except Exception as e:
        notes.append(f"JSON parse: failed ({type(e).__name__}: {e})")
        repaired = normalize({})

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(repaired, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    notes.append(f"Tags count after normalization: {len(repaired['tags'])}")
    notes.append(f"Confidence after normalization: {repaired['confidence']}")
    notes.append(f"Repair succeeded: {repair_succeeded}")

    report = "\n".join(notes) + "\n"
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(report)
    print(json.dumps(repaired, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
