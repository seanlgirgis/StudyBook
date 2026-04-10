# Practice Tracker

Purpose: run fast repetition loops and track confidence growth per problem.

Confidence scale:
- `1` = lost
- `2` = heavy hints needed
- `3` = workable with pauses
- `4` = mostly fluent
- `5` = interview-ready

## Current Batch (Basics First)

| Order | File | Status | Start Time | End Time | Result | Confidence (1-5) | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `002_lc_001_two_sum.py` | completed |  | 2026-04-08 09:04 | 3/3 passed | 5 | Hardest: picked wrong DS first (set/index idea), corrected to hash map |
| 2 | `005_lc_020_valid_parentheses.py` | completed |  | 2026-04-08 09:12 | 6/6 passed | 4 | Hardest: assembling logic quickly; memory muscle needs speed reps |
| 3 | `007_lc_704_binary_search.py` | completed |  | 2026-04-08 09:15 | 6/6 passed | 4 | Straightforward; needed little thinking, speed can improve |
| 4 | `012_lc_125_valid_palindrome.py` | completed |  | 2026-04-08 09:19 | 9/9 passed | 3 | Missed `l < r` guard in skip loop at first; also mixed up `lowercase()` vs `lower()` |
| 5 | `019_contains_duplicate_217.py` | completed |  | 2026-04-08 09:22 | 8/8 + 8/8 passed | 5 | No hiccups |
| 6 | `021_valid_anagram_242_empty.py` | completed |  | 2026-04-08 09:30 | 12/12 + 12/12 passed | 4 | ~5 min for both; stumbled on `all` call using `[]` instead of `()` |
| 7 | `020_product_except_self_238_empty.py` | completed |  | 2026-04-08 09:40 | 8/8 passed | 3 | Took ~14 min; first pass started prefix loop at 1 instead of 0; needs memory-muscle reps |
| 8 | `024_next_greater_single_list.py` | completed |  | 2026-04-08 09:48 | 10/10 passed | 4 | ~7.5 min; little struggle implementing monotonic increasing stack; wants auto-recall speed |

## Weak-Point Batch (Your Callout)

| Order | File | Status | Start Time | End Time | Result | Confidence (1-5) | Notes |
|---|---|---|---|---|---|---|---|
| 9 | `029_online_stock_span_901.py` | completed |  | 2026-04-08 09:54 | 5/5 passed | 2 | Had to look up answer; needs stronger monotonic stack visualization (inc/dec patterns) |
| 10 | `030_decode_ways_091_empty.py` | completed |  | 2026-04-08 10:00 | 13/13 passed | 1 | Looked up solution; needs ~10 reps for memory muscle |
| 11 | `031_coin_change_322_empty.py` | queued |  |  |  |  |  |
| 12 | `032_course_schedule_207_empty.py` | queued |  |  |  |  |  |

## Monotonic Focus Block (By Request)

| Order | File | Status | Start Time | End Time | Result | Confidence (1-5) | Notes |
|---|---|---|---|---|---|---|---|
| M1 | `024_next_greater_single_list.py` | completed |  | 2026-04-08 10:08 | 10/10 passed | 4 | Easier mental model; key insight: monotonic decreasing stack, pop smaller, store indices |
| M2 | `025_next_smaller_single_list.py` | completed |  | 2026-04-08 10:14 | 10/10 passed | 4 | Good run; polished for interview readability (stack type/comment/spacing) |
| M3 | `027_next_greater_element_496_empty.py` | completed |  | 2026-04-08 10:21 | 10/10 passed | 3 | Debug print removed; wants full monotonic block repetition |
| M4 | `028_lc_739_daily_temperatures.py` | completed |  | 2026-04-08 10:27 | 10/10 passed | 3-4 | Trigger phrase: `mono decreasing stack .. pop what is smaller than new .. store indexes` |
| M5 | `029_online_stock_span_901.py` | completed |  | 2026-04-08 10:39 | 5/5 passed | 4.5 | Smooth and confident; correctly used <= for equal-price span accumulation |




















| M6 | `011_lc_084_largest_rectangle_in_histogram.py` | completed |  | 2026-04-08 10:52 | 7/7 passed | 4.2 | No help needed; done many times, strong muscle memory |

## Two-Pointer Focus Block

| Order | File | Status | Start Time | End Time | Result | Confidence (1-5) | Notes |
|---|---|---|---|---|---|---|---|
| TP1 | 008_lc_042_trapping_rain_water.py | completed |  | 2026-04-08 10:58 | 5/5 passed | 4 | Solved with two-pointers + left/right max barriers; classify under two-pointer, not monotonic stack |

