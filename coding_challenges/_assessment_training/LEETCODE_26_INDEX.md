# LeetCode Practice Index (29 Cases + 1 Pattern Drill)

This index tracks the currently curated LeetCode problems and one additional monotonic-stack pattern drill in `coding_challenges/_assessment_training`.
Each section has:
- what the problem builds
- links to your local practice files for that case

Added monotonic-stack set:
- Next Greater Element (Monotonic Decreasing)
- Next Smaller Element (Monotonic Increasing pattern drill)
- Largest Rectangle in Histogram (Monotonic Increasing)
- Trapping Rain Water (Monotonic Decreasing stack variant)

## LC 1 - Two Sum
Builds hash-map complement lookup and one-pass reasoning. This is a core warm-up for array + hash patterns and interview explanation clarity.
- [two_sum_single_file.py](./two_sum/two_sum_single_file.py)
- [two_sum_review_drill.py](./review_pack/two_sum_review_drill.py)
- [two_sum_1_empty.py](./review_pack/round_01_empty/two_sum_1_empty.py)

## LC 3 - Longest Substring Without Repeating Characters
Builds sliding-window control (`left/right`) and set/map window membership updates. Good for pointer movement discipline.
- [longest_substring_without_repeating_3_empty.py](./review_pack/round_03_codesignal_remaining_15/longest_substring_without_repeating_3_empty.py)

## LC 15 - 3Sum
Builds sort + fixed-anchor + two-pointer scanning with duplicate skipping. This is a major pattern-composition problem.
- [three_sum_15_empty.py](./review_pack/round_02_empty/three_sum_15_empty.py)
- [three_sum_15_canonical_reference.py](./review_pack/round_02_empty/three_sum_15_canonical_reference.py)

## LC 20 - Valid Parentheses
Builds stack fundamentals and matching-map logic. Great for linear parsing and robust boundary checks.
- [valid_parentheses_single_file.py](./valid_parentheses/valid_parentheses_single_file.py)
- [valid_parentheses_review_drill.py](./review_pack/valid_parentheses_review_drill.py)
- [valid_parentheses_20_empty.py](./review_pack/round_01_empty/valid_parentheses_20_empty.py)

## LC 33 - Search in Rotated Sorted Array
Builds binary-search branch logic under partial ordering (one side sorted each step). Key for O(log n) decision trees.
- [search_rotated_sorted_array_33_empty.py](./review_pack/round_03_codesignal_remaining_15/search_rotated_sorted_array_33_empty.py)

## LC 42 - Trapping Rain Water
Builds valley-boundary reasoning and monotonic-stack index geometry (or two-pointer alternative). Strong for stack area calculations.
- [trapping_rain_water_42_empty.py](./review_pack/round_04_monotonic_stack/trapping_rain_water_42_empty.py)

## LC 49 - Group Anagrams
Builds signature-key grouping in hash maps (sorted key or char-frequency tuple key). Good for encoding structure into keys.
- [group_anagrams_review_drill.py](./review_pack/group_anagrams_review_drill.py)
- [group_anagrams_blank_practice.py](./review_pack/group_anagrams_blank_practice.py)
- [group_anagrams_49_empty.py](./review_pack/round_01_empty/group_anagrams_49_empty.py)

## LC 56 - Merge Intervals
Builds interval normalization via sort + linear merge scan. Strong for range reasoning and greedy compression.
- [merge_intervals_56_empty.py](./review_pack/round_03_codesignal_remaining_15/merge_intervals_56_empty.py)

## LC 84 - Largest Rectangle in Histogram
Builds monotonic increasing stack with width calculation from previous/next smaller boundaries.
- [largest_rectangle_in_histogram_84_empty.py](./review_pack/round_04_monotonic_stack/largest_rectangle_in_histogram_84_empty.py)

## LC 91 - Decode Ways
Builds DP over string positions with strict validity rules (`1..9`, `10..26`). Great for state transition practice.
- [decode_ways_91_empty.py](./review_pack/round_03_codesignal_remaining_15/decode_ways_91_empty.py)

## LC 125 - Valid Palindrome
Builds two-pointer filtering and normalization (`isalnum`, lowercase). Useful for string sanitation + in-place scanning.
- [valid_palindrome_125_empty.py](./review_pack/round_02_empty/valid_palindrome_125_empty.py)

## LC 128 - Longest Consecutive Sequence
Builds hash-set component start detection (`n-1 not in set`) and linear streak expansion.
- [longest_consecutive_128_review_drill.py](./review_pack/longest_consecutive_128_review_drill.py)
- [longest_consecutive_128_empty.py](./review_pack/round_01_empty/longest_consecutive_128_empty.py)

## LC 133 - Clone Graph
Builds graph deep-copy with old-to-new node mapping and cycle-safe DFS/BFS. Core graph object-cloning pattern.
- [clone_graph_133_empty.py](./review_pack/round_03_codesignal_remaining_15/clone_graph_133_empty.py)

## LC 146 - LRU Cache
Builds O(1) cache operations using hash map + doubly linked list recency ordering. Essential system-design-adjacent pattern.
- [lru_cache_146_empty.py](./review_pack/round_03_codesignal_remaining_15/lru_cache_146_empty.py)

## LC 155 - Min Stack
Builds constant-time minimum tracking with paired stack state. Good for augmented data-structure design.
- [min_stack_155_empty.py](./review_pack/round_03_codesignal_remaining_15/min_stack_155_empty.py)

## LC 167 - Two Sum II (Sorted Input)
Builds two-pointer arithmetic on sorted arrays plus 1-based index output discipline.
- [two_sum_ii_167_dual_empty.py](./review_pack/round_02_empty/two_sum_ii_167_dual_empty.py)

## LC 198 - House Robber
Builds 1D dynamic programming on adjacent-choice constraints (pick/skip). Strong transition to broader DP problems.
- [house_robber_198_empty.py](./review_pack/round_03_codesignal_remaining_15/house_robber_198_empty.py)

## LC 200 - Number of Islands
Builds component counting via DFS/BFS flood-fill on grids. Foundational graph traversal in matrix form.
- [number_of_islands_200_empty.py](./review_pack/round_03_codesignal_remaining_15/number_of_islands_200_empty.py)

## LC 207 - Course Schedule
Builds directed cycle detection (DFS states or topo sort). Core prerequisite/dependency graph reasoning.
- [course_schedule_207_empty.py](./review_pack/round_03_codesignal_remaining_15/course_schedule_207_empty.py)

## LC 215 - Kth Largest Element in an Array
Builds heap/selection strategies and tradeoff awareness (`O(n log k)` vs `O(n + k log n)`).
- [kth_largest_element_215_empty.py](./review_pack/round_03_codesignal_remaining_15/kth_largest_element_215_empty.py)

## LC 217 - Contains Duplicate
Builds fast membership with sets and complexity contrast (`O(n)` vs `O(n^2)` with list lookup).
- [contains_duplicate_217_empty.py](./review_pack/round_02_empty/contains_duplicate_217_empty.py)

## LC 238 - Product of Array Except Self
Builds prefix/suffix accumulation and no-division constraints with O(1) extra-space style.
- [product_except_self_238_review_drill.py](./review_pack/product_except_self_238_review_drill.py)
- [product_except_self_238_empty.py](./review_pack/round_01_empty/product_except_self_238_empty.py)

## LC 242 - Valid Anagram
Builds frequency-count validation and string normalization assumptions (usually lowercase letters).
- [valid_anagram_242_empty.py](./review_pack/round_02_empty/valid_anagram_242_empty.py)

## LC 295 - Find Median from Data Stream
Builds two-heap balancing (max-left/min-right) and median extraction by parity.
- [find_median_data_stream_295_empty.py](./review_pack/round_03_codesignal_remaining_15/find_median_data_stream_295_empty.py)

## LC 300 - Longest Increasing Subsequence
Builds dynamic programming (and optionally patience sorting + binary search variant). Strong subsequence DP pattern.
- [longest_increasing_subsequence_300_empty.py](./review_pack/round_03_codesignal_remaining_15/longest_increasing_subsequence_300_empty.py)

## LC 322 - Coin Change
Builds minimum-steps DP with impossible-state handling; includes bottom-up, top-down, and BFS variants.
- [coin_change_322_empty.py](./review_pack/round_03_codesignal_remaining_15/coin_change_322_empty.py)

## LC 347 - Top K Frequent Elements
Builds frequency counting + either bucket strategy (`O(n)`) or heap strategy (`O(n log k)`).
- [top_k_frequent_single_file.py](./top_k_frequent_elements/top_k_frequent_single_file.py)
- [top_k_frequent_minheap_single_file.py](./top_k_frequent_elements/top_k_frequent_minheap_single_file.py)
- [top_k_frequent_minheap_single_file_my_practice.py](./top_k_frequent_elements/top_k_frequent_minheap_single_file_my_practice.py)
- [top_k_frequent_blank_practice.py](./top_k_frequent_elements/top_k_frequent_blank_practice.py)
- [top_k_frequent_blank_practice_minheap.py](./top_k_frequent_elements/top_k_frequent_blank_practice_minheap.py)
- [top_k_frequent_347_review_drill.py](./review_pack/top_k_frequent_347_review_drill.py)
- [top_k_frequent_347_empty.py](./review_pack/round_01_empty/top_k_frequent_347_empty.py)

## LC 496 - Next Greater Element I
Builds monotonic decreasing stack map construction from `nums2` to answer queries in `nums1`.
- [next_greater_element_496_empty.py](./review_pack/round_04_monotonic_stack/next_greater_element_496_empty.py)

## LC 739 - Daily Temperatures
Builds monotonic-stack pattern for next-greater-element style problems in linear time.
- [daily_temperatures_739_empty.py](./review_pack/round_03_codesignal_remaining_15/daily_temperatures_739_empty.py)

## Pattern Drill - Next Smaller Element
Builds monotonic increasing stack behavior for first-smaller-to-right queries. Good complement to next-greater patterns.
- [next_smaller_element_pattern_empty.py](./review_pack/round_04_monotonic_stack/next_smaller_element_pattern_empty.py)
