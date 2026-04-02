# Study Manual v1 (Coding Challenges)

Generated: 2026-04-02
Source basis:
- `D:\StudyBook\coding_challenges\INDEX.md`
- `D:\StudyBook\coding_challenges\ROADMAP_INPUT_MANIFEST.md`
- `D:\StudyBook\coding_challenges\leetcode\TOPIC_COVERAGE.md`

## 1) What To Study From

Use these folders in this order:
1. `leetcode/by_topic` (curated solved references)
2. `guides` (concept deep dives)
3. `leetcode/active` (daily notebook execution/practice)
4. `leetcode/reviews` (problem-by-problem review notes)
5. `python` (fundamentals + data libraries)
6. `study_plans` (day templates and historical plans)

## 2) Daily Operating Loop (90-120 mins)

1. Warm-up (10 min)
- Pick 1 prior solved file from `leetcode/by_topic/<topic>` and summarize approach from memory.

2. Concept refresh (20 min)
- Open one guide notebook under `guides/...` that matches today topic.
- Write 3 bullets: pattern, complexity, common mistakes.

3. Timed coding block (35-45 min)
- Solve 1-2 problems in `leetcode/active` without opening prior answers first.
- Use prior solution only for post-attempt gap analysis.

4. Review and annotate (20 min)
- Update or create a corresponding note in `leetcode/reviews` format.
- Add: brute force baseline, optimal approach, complexity, edge cases.

5. Python reinforcement (10-15 min)
- Rotate between:
  - `python/fundamentals/nuggets.md`
  - `python/data_libraries/*`
- Add one reusable snippet into your own notes.

## 3) Weekly Cadence

- 5 focused practice days
- 1 consolidation day
- 1 mock/interview day

Consolidation day:
- Re-solve 3 missed or slow problems from the week.
- Update one guide summary page in your notes.

Mock day:
- 2 timed questions (45 min each).
- 1 verbal explanation round (problem + tradeoffs + complexity).

## 4) Topic Priority (from current coverage)

Current strongest repository depth:
- graphs (25)
- dynamic_programming (19)
- stack (10)

Medium depth:
- hashing (8), heaps (7), intervals (7), trees (7), binary_search (6)

Lower depth / should be reinforced:
- arrays (3), sliding_window (3), two_pointers (4), bit_manipulation (5), linked_list (5), mixed (5)

Priority rule:
- Keep strengths warm with 30-40% of time.
- Spend 60-70% on lower/medium depth areas until balanced.

## 5) Quality Standard For Each Solved Problem

A problem is "complete" only when all are true:
- You can restate the problem in 2-3 lines.
- You can explain brute force and why it is suboptimal.
- You can implement optimal solution cleanly.
- You can state time/space complexity confidently.
- You can list 2-3 edge cases and pass them.

## 6) Roadmap Input Usage

Use `ROADMAP_INPUT_MANIFEST.md` and `_migration_meta/run_20260402_113935/*` as source-of-truth for:
- topic distribution
- migration integrity evidence
- future manual/roadmap regeneration

## 7) Next Manual Iterations

Planned upgrades in v2:
- Add track-by-track weekly assignments tied to exact files.
- Add difficulty ladder per topic (easy -> medium -> hard).
- Add KPI dashboard template (speed, accuracy, confidence).
