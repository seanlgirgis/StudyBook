# Round 05 Study Map

Purpose: quick-reference map of exercises in this folder, grouped by concept/data structure and ordered from easier to harder inside each group.

## 1) Hashing and Frequency Basics

### Easy
- `002_lc_001_two_sum.py`
  - Idea: complement lookup in one pass.
  - Concepts touched: hash map, O(n) lookup, index tracking.
- `019_contains_duplicate_217.py`
  - Idea: detect duplicate via set membership.
  - Concepts touched: set uniqueness, early return vs full pass.
- `021_valid_anagram_242_empty.py`
  - Idea: compare character frequencies.
  - Concepts touched: fixed-size counting array, hashing alternative.

### Medium
- `009_lc_049_group_anagrams.py`
  - Idea: build signature key per word then group.
  - Concepts touched: frequency tuple key, hash map of buckets.
- `013_longest_consecutive_128_review_drill.py`
  - Idea: detect sequence starts with `n-1 not in set`.
  - Concepts touched: set lookup, component-growth in O(n).

## 2) Two Pointers and String Window

### Easy
- `012_lc_125_valid_palindrome.py`
  - Idea: skip non-alnum chars from both ends.
  - Concepts touched: two pointers, normalization, in-place scan.

### Medium
- `004_lc_003_longest_substring_without_repeating.py`
  - Idea: sliding window with set and left shrink.
  - Concepts touched: window invariants, duplicate eviction.
- `015_two_sum_ii_167_dual_empty.py`
  - Idea: sorted-array two pointers.
  - Concepts touched: order-aware pointer movement, 1-based indexing.
- `003_lc_015_three_sum.py`
  - Idea: sort + anchor + two pointers + dedupe.
  - Concepts touched: duplicate control, pair-sum inside loop.

## 3) Binary Search and Ordered Reasoning

### Easy
- `007_lc_704_binary_search.py`
  - Idea: halve search space each step.
  - Concepts touched: loop invariants, left/right boundary updates.

### Medium
- `006_lc_033_search_rotated_sorted_array.py`
  - Idea: one half is always sorted, decide side by target range.
  - Concepts touched: conditional binary-search branches.

## 4) Stack and Monotonic Stack Patterns

### Easy
- `005_lc_020_valid_parentheses.py`
  - Idea: closing bracket must match stack top opener.
  - Concepts touched: stack discipline, parsing rules.
- `027_next_greater_element_496_empty.py`
  - Idea: monotonic decreasing stack over source array.
  - Concepts touched: next-greater mapping, index/value resolution.
- `024_next_greater_single_list.py` (custom)
  - Idea: first greater value to the right.
  - Concepts touched: monotonic stack, unresolved indices.
- `025_next_smaller_single_list.py` (custom)
  - Idea: first smaller value to the right.
  - Concepts touched: inverted monotonic condition.

### Medium
- `028_lc_739_daily_temperatures.py`
  - Idea: unresolved colder days wait on stack until warmer day arrives.
  - Concepts touched: next-greater distances, index arithmetic.
- `026_lc_503_next_greater_element_ii.py`
  - Idea: simulate circular array by iterating twice.
  - Concepts touched: modulo indexing, monotonic stack in circular context.
- `029_online_stock_span_901.py`
  - Idea: collapse weaker previous days to compute span quickly.
  - Concepts touched: monotonic stack with aggregated spans.

### Hard
- `011_lc_084_largest_rectangle_in_histogram.py`
  - Idea: when height drops, finalize rectangles for popped bars.
  - Concepts touched: monotonic increasing stack, width boundaries.

## 5) Intervals and Array Product

### Medium
- `010_lc_056_merge_intervals.py`
  - Idea: sort by start, merge overlaps greedily.
  - Concepts touched: interval normalization, accumulator pattern.
- `020_product_except_self_238_empty.py`
  - Idea: prefix product pass + postfix product pass.
  - Concepts touched: O(n) no-division design, in-place result build.

## 6) Dynamic Programming

### Medium
- `016_lc_198_house_robber.py`
  - Idea: at each house choose rob/skip max transition.
  - Concepts touched: rolling DP states, adjacency constraint.
- `022_longest_increasing_subsequence_300_empty.py`
  - Idea: `dp[i]` is LIS ending at `i`.
  - Concepts touched: subsequence DP, transition from previous indices.
- `030_decode_ways_091_empty.py`
  - Idea: one-digit and two-digit valid decode transitions.
  - Concepts touched: DP over string positions, zero handling.
- `031_coin_change_322_empty.py`
  - Idea: min coins for remaining amount with memoized DFS.
  - Concepts touched: top-down DP, impossible-state sentinel.

## 7) Heap / Priority Queue

### Medium
- `018_lc_215_kth_largest_element.py`
  - Idea: keep size-k min-heap of largest seen values.
  - Concepts touched: heap pruning, kth-order statistic.
- `023_top_k_frequent_elements_347_empty.py`
  - Idea: count frequencies then keep top-k by min-heap.
  - Concepts touched: Counter + heap, top-k pattern.
- `001_lc_295_find_median_from_data_stream.py`
  - Idea: two heaps balance lower/upper halves.
  - Concepts touched: max-heap/min-heap coordination, median extraction.

## 8) Graph / Grid Traversal

### Easy
- `038_lc_733_flood_fill.py`
  - Idea: BFS/DFS expand from seed color region.
  - Concepts touched: grid traversal, visited-by-recoloring.
- `039_lc_994_rotting_oranges.py`
  - Idea: multi-source BFS, each layer = 1 minute.
  - Concepts touched: queue levels, shortest-time spread.

### Medium
- `017_lc_200_number_of_islands.py`
  - Idea: count components via DFS sink.
  - Concepts touched: graph in grid, component counting.
- `032_course_schedule_207_empty.py`
  - Idea: detect cycle in directed prerequisite graph.
  - Concepts touched: DFS states (unvisited/visiting/done).
- `033_clone_graph_133_empty.py`
  - Idea: clone nodes with old->new map to handle cycles.
  - Concepts touched: graph DFS, deep copy with memo map.

## 9) Tree Fundamentals

### Easy
- `036_lc_104_maximum_depth_of_binary_tree.py`
  - Idea: recursive depth = `1 + max(left, right)`.
  - Concepts touched: tree recursion, base case reasoning.

### Medium
- `035_lc_102_binary_tree_level_order_traversal.py`
  - Idea: BFS level by level.
  - Concepts touched: queue breadth traversal, level batching.

## 10) Design Data Structures

### Medium
- `014_min_stack_155_empty.py`
  - Idea: stack + min-stack for O(1) minimum.
  - Concepts touched: augmented stack state.
- `034_lru_cache_146_empty.py`
  - Idea: hash map + doubly linked list recency timeline.
  - Concepts touched: O(1) get/put with eviction policy.

## 11) Foundation Wrappers (Data Structure Drills)

### Easy to Medium
- `040_doubly_linked_list_foundation_exercise.py`
  - Idea: practice pointer rewiring with sentinel head/tail and integrity checks.
  - Concepts touched: node insertion/removal, front/back operations, structural invariants.
- `041_min_heap_wrapper_foundation_exercise.py`
  - Idea: wrap `heapq` as a clean min-heap API with behavior tests.
  - Concepts touched: heap push/pop/peek, empty-state handling, state validation harness.
- `042_max_heap_wrapper_foundation_exercise.py`
  - Idea: build max-heap wrapper via negation over `heapq`.
  - Concepts touched: min-heap adaptation to max-heap, API symmetry, exception coverage.

## Suggested Last-Day Focus (High Yield)

1. `002`, `005`, `007`, `015`, `016`, `020` (fast confidence set)
2. `028`, `023`, `018`, `030`, `031` (timed-core set)
3. `032`, `033`, `035`, `038`, `039` (graph/tree coverage set)
