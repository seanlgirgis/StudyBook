import json
import re
import time
from pathlib import Path
from urllib import request

BASE_URL = "http://localhost:8002"
INFER_URL = BASE_URL + "/infer"
TIMEOUT_SECONDS = 180

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "memory_blobs.jsonl"
OUT_DIR = BASE_DIR / "outputs"
LOCAL_CANDIDATES_OUT = OUT_DIR / "local_candidates.json"
AI_PROMPT_OUT = OUT_DIR / "ai_rerank_prompt.txt"
AI_RAW_OUT = OUT_DIR / "ai_rerank_raw.txt"
FINAL_REPORT_OUT = OUT_DIR / "final_search_report.txt"

QUERY = "Find the financial data engineer job I applied for around February 2026."
IMPORTANT_WORDS = {
    "financial", "finance", "banking", "data", "engineer", "job",
    "application", "february", "2026", "recruiter", "pyspark", "sql", "etl",
}


def tokenize(text: str):
    return re.findall(r"[a-z0-9]+", text.lower())


def load_blobs(path: Path):
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        items.append(json.loads(line))
    return items


def local_score(item: dict, query_tokens: set):
    text = f"{item.get('title', '')} {item.get('memory_blob', '')}".lower()
    item_tokens = set(tokenize(text))
    overlap = query_tokens.intersection(item_tokens)

    base = len(overlap)
    bonus = sum(2 for w in overlap if w in IMPORTANT_WORDS)
    score = base + bonus
    return score, sorted(overlap)


def post_infer(prompt: str):
    payload = {"query": prompt}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(INFER_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def short_blob(text: str, max_len: int = 300):
    t = text.strip()
    return t[:max_len] + ("..." if len(t) > max_len else "")


def build_rerank_prompt(candidates: list[dict]):
    letters = ["A", "B", "C"]
    lines = []
    lines.append("You are ranking search results.")
    lines.append("")
    lines.append("User query:")
    lines.append(QUERY)
    lines.append("")
    lines.append("Candidates:")

    for i, c in enumerate(candidates):
        lines.append(f"{letters[i]}) {c['vault_item_id']} - {c['title']}")
        lines.append(short_blob(c["memory_blob"]))
        lines.append("")

    lines.append("Pick the best candidate.")
    lines.append("Then explain why in 1 short sentence.")
    lines.append("")
    lines.append("Format:")
    lines.append("BEST: <vault_item_id>")
    lines.append("WHY: <short reason>")
    return "\n".join(lines)


def extract_best_id(ai_text: str):
    m = re.search(r"BEST:\s*([a-zA-Z0-9\-]+)", ai_text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else ""


def main():
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    items = load_blobs(DATA_FILE)
    query_tokens = set(tokenize(QUERY))

    scored = []
    for item in items:
        score, overlap = local_score(item, query_tokens)
        scored.append({
            "vault_item_id": item["vault_item_id"],
            "title": item["title"],
            "source_location": item["source_location"],
            "memory_blob": item["memory_blob"],
            "local_score": score,
            "overlap_words": overlap,
        })

    scored.sort(key=lambda x: x["local_score"], reverse=True)
    top_candidates = scored[:3]
    LOCAL_CANDIDATES_OUT.write_text(json.dumps(top_candidates, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    infer_worked = False
    ai_text = ""
    ai_empty = True
    final_selected = top_candidates[0]["vault_item_id"] if top_candidates else "(none)"
    fallback_note = ""

    prompt = build_rerank_prompt(top_candidates)
    AI_PROMPT_OUT.write_text(prompt + "\n", encoding="utf-8")

    try:
        status, body = post_infer(prompt)
        infer_worked = 200 <= status < 300
        if not infer_worked:
            raise RuntimeError(f"HTTP {status}: {body[:1000]}")

        api_obj = json.loads(body)
        ai_text = str(api_obj.get("answer", "")).strip()
        ai_empty = (ai_text == "")
        AI_RAW_OUT.write_text(ai_text + "\n", encoding="utf-8")

        if ai_empty:
            fallback_note = "AI rerank was empty; used local top candidate."
        else:
            best_id = extract_best_id(ai_text)
            candidate_ids = {c["vault_item_id"] for c in top_candidates}
            if best_id in candidate_ids:
                final_selected = best_id
            else:
                fallback_note = "AI BEST id missing/invalid; used local top candidate."

    except Exception as e:
        ai_text = f"ERROR: {type(e).__name__}: {e}"
        ai_empty = True
        fallback_note = "AI rerank was empty; used local top candidate."
        AI_RAW_OUT.write_text(ai_text + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - start

    lines = []
    lines.append("LifeVault Blob Search + AI Rerank Report")
    lines.append("=" * 60)
    lines.append(f"Original query: {QUERY}")
    lines.append(f"Infer worked: {infer_worked}")
    lines.append(f"Elapsed seconds: {elapsed:.2f}")
    lines.append("-")
    lines.append("Local top candidates:")
    for c in top_candidates:
        lines.append(f"- {c['vault_item_id']} | score={c['local_score']} | title={c['title']} | overlap={', '.join(c['overlap_words'])}")
    lines.append("-")
    lines.append("Raw AI rerank response:")
    lines.append(ai_text)
    lines.append("-")
    lines.append(f"AI response empty: {ai_empty}")
    if fallback_note:
        lines.append(f"Fallback: {fallback_note}")
    lines.append(f"Final selected item: {final_selected}")

    report_text = "\n".join(lines) + "\n"
    FINAL_REPORT_OUT.write_text(report_text, encoding="utf-8")
    print(report_text)


if __name__ == "__main__":
    main()
