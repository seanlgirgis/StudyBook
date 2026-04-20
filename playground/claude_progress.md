# CodeSignal GCA Practice — Claude's Progress Log
> Keeper: Claude | Updated before every new question | Living document — never frozen
> **Notebook rules:** Every new notebook must include `%run _timer.py` as the second cell (after markdown, before solution). Sean records solve time as `# solved in MM:SS` on the first line of his solution.

---

## Context
Sean is preparing for a **Capital One CodeSignal GCA** (70 min, 4 questions, Python 3).  
Recruiter (Sam) flagged key topics: **2D arrays/matrices**, **HashMaps**, **DSA**.  
Q1/Q2 are warm-ups. Q3/Q4 are medium/hard.  
This is a **continuous project** — beyond the test, toward mastery.

---

## Problem Library

| # | Name | Topic | Status | Notes |
|---|------|--------|--------|-------|
| 0001 | key_changes | String, counting | ✅ | -1 trick, case-insensitive |
| 0002 | battery_swap | Heapq, cyclic | ✅ | Two heaps: ready + recovering |
| 0003 | zigzag | Array patterns | ✅ | Detect peaks/valleys |
| 0004 | harmonious_structures | Vector math | ✅ | zip, stepwise +1 |
| 0005 | drone_delivery | Simulation | ✅ | Range=10, nearest station |
| 0006 | channel_surfing | Spaced repeat 0001 | ✅ | |
| 0007 | terrain_analysis | Spaced repeat 0003 | ✅ | |
| 0008 | stepped_podium | Spaced repeat 0004 | ✅ | Step size=2 |
| 0009 | fuel_stops | Spaced repeat 0005 | ✅ | Min stops, jump farthest |
| 0010 | relay_runners | Spaced repeat 0002 | ✅ | |
| 0011 | diagonal_difference | 2D matrix | ✅ | Primary vs secondary diagonal |
| 0012 | first_unique | HashMap / Counter | ✅ | Two-pass Counter pattern |
| 0013 | border_sum | 2D boundary | ✅ | Set union of 4 edges |
| 0014 | two_sum | HashMap O(n) | ✅ | seen dict, complement lookup |
| 0015 | column_sums | 2D column traversal | ✅ | `zip(*matrix)` discovered |
| 0016 | transpose | 2D zip* | ✅ | `[list(col) for col in zip(*matrix)]` |
| 0017 | max_subarray | Kadane's | ✅ | extend or restart |
| 0018 | valid_anagram | Counter / array[26] | ✅ | Sean used fixed array — deep insight |
| 0019 | running_sum | Prefix sums | ✅ | `accumulate` introduced |
| 0020 | max_window_sum | Fixed sliding window | ✅ | double-exclusive `n+1` |
| 0021 | min_subarray | Spaced repeat 0017 | ✅ | Kadane's flipped |
| 0022 | most_frequent | Counter + heap/key | ✅ | `(-freq, num)` tuple trick |
| 0023 | product_except_self | Prefix/suffix product | ✅ | Jumped straight to O(n) |
| 0024 | sorted_squares | Two pointers (intro) | ✅ | Used heap — O(n log n); one-liner `sorted(x**2 for x in nums)` also shown |
| 0025 | is_palindrome | Two pointers spaced repeat | ✅ | closing inward; `s[::-1]` one-liner also shown — remind Sean of slice reversal |
| 0026 | merge_sorted | Two pointers advancing | ✅ | extend tail-flush pattern |
| 0027 | binary_search | Binary search intro | ✅ | used overflow-safe mid; clean textbook solution |
| 0028 | search_insert | Binary search spaced repeat | ✅ | return l — l lands at insertion point |
| 0029 | group_anagrams | HashMap group-by | ✅ | freq array key — same insight as 0018; setdefault over defaultdict |
| 0030 | longest_unique | Variable sliding window | ✅ | 8:43 — clean inner-while shrink; `not s` > `len(s)==0` |
| 0031 | valid_parentheses | Stack intro | ✅ | 9:44 — textbook; two ifs collapsed to one with `or` |
| 0032 | min_stack | Stack design | ✅ | tuple (val, min_so_far) — elegant single-stack; caught double-push bug |
| 0033 | matrix_rotation | 2D transform | ✅ | 12:36 — transpose + row.reverse(); `[::-1]` not in-place |
| 0034 | spiral_order | 2D boundary advanced | ✅ | pop+rotate CCW trick; peel top, rotate remaining |
| 0035 | subarray_sum_k | Prefix sum + HashMap | ✅ | brute O(n²) solved; O(n) shown — query before store is critical |
| 0036 | top_k_frequent | Counter + size-k heap | ✅ | 7:27 — O(n log k) size-k min-heap; `most_common(k)` one-liner shown |
| 0037 | longest_consecutive | Set + streak counting | ✅ | 3:52 — fastest solve yet; straight to O(n) optimal |
| 0038 | three_sum | Two sum extended | ✅ | 14:30 — HashMap approach + set dedup; two-pointer alternative shown |
| 0039 | container_water | Two pointers greedy | ✅ | 6:47 — advance shorter wall; clean O(n) |
| 0040 | climbing_stairs | Dynamic programming intro | ✅ | 3:00 — Fibonacci pattern; O(1) space two-variable solution |
| 0041 | house_robber | DP spaced repeat | ✅ | 4:00 — same two-variable pattern as climbing stairs; internalized |
| 0042 | coin_change | DP bottom-up | ✅ | needed debug help — inf seed + indent bug; pattern now locked |
| 0043 | unique_paths | 2D DP | ✅ | needed table visual to unlock; solved immediately after |
| 0044 | min_path_sum | 2D DP spaced repeat | ✅ | needed edge-seeding reminder; solved correctly after |
| 0045 | find_disappeared | Set difference | ✅ | 7:12 — loop over range approach; good O(n) instinct |
| 0046 | majority_element | Counter / Boyer-Moore | ✅ | Counter.most_common(1)[0][0]; Boyer-Moore shown as bonus |
| 0047 | best_time_stock | Running min / greedy | ✅ | track min buy price + max profit in one pass |
| 0048 | linked_list_reverse | Linked list intro | ✅ | prev/curr/nxt pattern; while curr not curr.next; return prev |
| 0049 | middle_linked_list | Linked list traversal | ✅ | two-pass: count n, then walk n//2 steps |
| 0050 | linked_list_cycle | Linked list / seen set | ✅ | id(node) in set — O(n) space; Floyd's fast-slow is O(1) space bonus |
| 0051 | merge_two_sorted_lists | Linked list merge | ✅ | dummy+tail pattern; rewire .next, flush remainder with tail.next = curr1 or curr2 |
| 0052 | remove_nth_from_end | Linked list / two pointers | ✅ | two-pass: get length, delete at (length - n); delete_at_index added to basics |
| 0053 | palindrome_linked_list | Linked list + reverse | ✅ | collect vals to list, compare vals == vals[::-1] |
| 0054 | number_of_islands | 2D grid / DFS flood fill | ✅ | 13:25 — floodIt sinks connected land to '0'; directions pattern |
| 0055 | max_area_island | 2D grid DFS spaced repeat | ✅ | floodIt returns area count; fixed bad assertion (5 not 6) |
| 0056 | flood_fill | 2D grid DFS / image processing | ✅ | 10:20 — same-color early return; pass cur_color to recurse on original color only |
| 0057 | rotting_oranges | 2D grid / BFS | ✅ | multi-source BFS; timestamp in queue tuple; clock = max(clock, t+1); -1 if fresh > 0 |
| 0058 | word_search | 2D grid DFS backtracking | 🔲 | looked up — backtracking + path set new; good to see, not drilling |
| 0059 | score_tracker | Simulation / HashMap | ✅ | defaultdict + sorted with (-score, name) tuple key |
| 0060 | task_scheduler_sim | Simulation | ✅ | running clock + parse split — clean Q1 pattern |
| 0061 | longest_subarray_ones | Sliding window variable | ✅ | at most one 0 in window; right-left not +1 = mandatory deletion baked in |
| 0062 | max_consecutive_ones | Sliding window spaced repeat | ✅ | same as 0061 but k zeros allowed; right-left+1 (keeping zeros, not deleting) |
| 0063 | ransom_note | HashMap spaced repeat | ✅ | Counter + mag[c] < freq (not !=); extra letters in magazine are fine |
| 0064 | min_operations_array | Simulation / greedy | ✅ | prev+1-num ops per step; prev=num+ops; Sean caught bad assertion on [3,2,1] |
| 0065 | k_closest_points | Heapq size-k | ✅ | max-heap with -dist; same pattern as top_k_frequent |
| 0066 | matrix_zero | 2D matrix in-place | ✅ | collect zeros first then apply — avoids cascading; Sean caught bad assertion again |
| 0067 | jump_game | Greedy / max_reach | ✅ | last element unused; if i > max_reach return False; last index value irrelevant |
| 0068 | string_compression | Simulation / run-length encoding | ✅ | track ch+cnt, flush on change and at end; skip count if 1 |
| 0069 | pivot_index | Prefix sum spaced repeat | ✅ | right = total - left - nums[i]; Sean caught bad [1,0] assertion |
| 0070 | decode_string | Stack / simulation | ✅ | push all chars; on ] pop alpha+[+digits backwards; multi-digit handled by reversing popped digits |
| 0071 | num_recent_calls | Deque / sliding window | ✅ | drop from left while t-q[0]>3000, append, return len |
| 0072 | min_cost_climbing | DP spaced repeat | ✅ | min(prev,prevprev) at end — same two-var as climbing_stairs |
| 0073 | find_anagrams | Sliding window + Counter | ✅ | [0]*26 fixed array; O(n·m) rebuild each step — O(n) possible by sliding in/out |
| 0074 | longest_palindrome_substr | Two pointers / expand center | ✅ | odd pivot (seed=s[x]) + even pivot (seed=""); unified helper: expand(i,j), return s[i+1:j] |
| 0075 | search_2d_matrix | Binary search | ✅ | flat index: row=mid//n, col=mid%n; itemAt helper keeps loop clean |
| 0076 | valid_sudoku | 2D matrix + HashMap/Set | ✅ | closure get_sub_matrix; valid_list reused for rows+cols; zip(*board) for columns |
| 0077 | max_depth_binary_tree | Tree / BFS with depth tuple | ✅ | deque[(node,depth)]; update max on push; return 0 not bare return for None |
| 0078 | invert_binary_tree | Tree / BFS | ✅ | BFS swap; node.left,node.right=node.right,node.left avoids dummy var |
| 0079 | symmetric_tree | Tree / recursion | ✅ | is_mirror(l,r): crossover l.left↔r.right, l.right↔r.left; level palindrome approach fails |
| 0080 | level_order_traversal | Tree / BFS | ✅ | snapshot len(queue), inner loop collects one level; pattern now internalized |
| 0081 | validate_bst | Tree / recursion + bounds | ✅ | compare_all BFS helper O(n²); O(n) alt: is_valid(node,lo,hi) passing bounds down |
| 0082 | lowest_common_ancestor | BST property | ✅ | both > curr → right; both < curr → left; else = split point or match → return curr.val |
| 0083 | path_sum | Tree / DFS recursion | ✅ | subtract val each level; leaf check: not left and not right; return remainder==0 |
| 0084 | count_good_nodes | Tree / DFS + running max | ✅ | dfs(node, max_so_far); seed with root.val (root always good); count if val>=max |
| 0085 | kth_smallest_bst | BST / inorder | ✅ | iterative inorder with stack; push all lefts, pop+decrement, exit at k==0; O(k) not O(n) |
| 0086 | right_side_view | Tree / BFS level order | ✅ | level BFS; append node.val when i==n-1 (last in level) |
| 0087 | diameter_binary_tree | Tree / DFS post-order | ✅ | nonlocal self_max; return height up, update diameter sideways (left+right) |
| 0088 | merge_intervals | Sort + sweep | ✅ | sort, seed out with first; mergeIt: overlap → extend end with max; else append |
| 0089 | single_number | XOR / bit trick | ✅ | res^=n; pairs cancel (n^n=0), survivor remains (n^0=n) |
| 0090 | missing_number | Math / set | ✅ | set lookup; alt: n*(n+1)//2 - sum(nums) |
| 0091 | move_zeroes | Two pointers | ✅ | l=insert pointer; swap nums[l],nums[r] when r!=0; l advances only on non-zero |
| 0092 | happy_number | Set / cycle detection | ✅ | seen set; while n!=1 and n not in seen; return n==1 |
| 0093 | course_schedule | Graph / DFS cycle detection | ✅ | 3-state DFS: 0=unvisited,1=visiting,2=done; state[i]==1 = back edge = cycle |
| 0094 | subsets | Backtracking | ✅ | backtrack(i,path): skip or include; base case i==len(nums) → append copy |
| 0095 | longest_common_prefix | String | ✅ | enumerate first string; inner loop checks all others at same index; return pref on mismatch |
| 0096 | number_of_1_bits | Bit manipulation | ✅ | n&1 + right shift; n&(n-1) strips lowest set bit; bin(n).count('1') one-liner |
| 0097 | reverse_string | String / two pointers | ✅ | l,r closing inward; swap s[l],s[r]; while r>l |
| 0098 | valid_palindrome | String / two pointers | ✅ | skip non-alnum in-place; isalnum()+lower(); two pointers closing inward |
| 0099 | find_peak_element | Array / linear scan | ✅ | global max is always a peak; return nums.index(max(nums)) |
| 0100 | climbing_stairs_variants | DP spaced repeat | ✅ | two-var rolling DP; current = cost[i] + min(prevprev, prev); return min of last two |


| 0101 | daily_temperatures | Monotonic stack (decreasing) | ✅ | store indices; pop when val > top; ans[idx] = i - idx |
| 0102 | next_greater_element | Monotonic stack repeat | 🔲 | — |
| 0103 | find_min_rotated | Binary search variant | 🔲 | — |

**Spaced repeats due (not yet written):**
- 0021 is min_subarray (spaced repeat of 0017) ✅
- Spaced repeat of 0021 (Kadane's) — deferred by Sean, schedule later
- Spaced repeat of 0020 (sliding window) — pending
- Spaced repeat of 0023 (prefix/suffix) — pending

---

## Topics Covered

| Topic | Introduced | Spaced Repeat |
|-------|-----------|---------------|
| String counting | 0001 | 0006 |
| Heapq / cyclic | 0002 | 0010 |
| Array patterns | 0003 | 0007 |
| Vector math / zip | 0004 | 0008 |
| Simulation | 0005 | 0009 |
| 2D matrix — diagonals | 0011 | — |
| HashMap / Counter | 0012 | 0014, 0022 |
| 2D boundary traversal | 0013 | — |
| Two sum / complement | 0014 | — |
| 2D column traversal / zip* | 0015 | 0016 |
| Kadane's (max/min subarray) | 0017 | 0021 |
| Fixed array vs HashMap | 0018 | — |
| Prefix sums | 0019 | — |
| Sliding window (fixed) | 0020 | — |
| Prefix/suffix products | 0023 | — |
| Two pointers | 0024 | — |

---

## Path Forward (Planned Topics)

- **Two pointers** — 0024 ✅, 0025 ✅, 0026 ✅
- **Binary search** — 0027 (next)
- **Matrix spiral traversal** — 2D boundary advanced
- **Matrix rotation 90°** — 2D transform
- **HashMap: group by key** — e.g. group anagrams
- **Sliding window variable size** — longest substring without repeat
- **Stack** — valid parentheses, next greater element
- **Sorting with key** — multi-criteria sort
- **Spaced repeats** — revisit Kadane's, sliding window, prefix sums as needed

---

## How Sean Thinks — Style Profile

**Strengths:**
- Reaches for the right data structure fast (Counter, heap, set)
- Builds clean, minimal code — no unnecessary scaffolding
- Jumps to O(n) solutions directly when the pattern clicks (see: product_except_self)
- Uses `(-freq, num)` tuple trick for multi-criteria ordering — natural heap thinking
- Fixed char array [0]*26 for anagram — shows real memory awareness
- Set union `|` for boundary problems — elegant dedup thinking

**Characteristic patterns Sean uses:**
- `-1 trick` for counting (start at -1, first item cancels it)
- `zip` and generator expressions over intermediate lists
- `heapq` with `ticket_counter` for cyclic ordering
- Two heaps: `ready` + `recovering` (battery_swap pattern)

**How Sean learns:**
- Solves brute force first, then asks about the optimal — organic progression
- Asks short, sharp questions when something is new (`what is | here`, `why n+1`)
- Does not need long explanations — a trace or one example unlocks it
- When stuck, says so directly (`I am stuck`, `not understanding kadene`)
- Confirms understanding with action, not words — just submits the solution

---

## Struggles & Watchpoints
> These are things to reinforce through spaced repetition and careful explanation

| Area | What happened | How to help |
|------|--------------|-------------|
| `sum` shadows builtin | Used `sum = 0` then called `sum(...)` — TypeError | Remind at start of new problems that use accumulation |
| Sliding window off-by-one | Used `range(k, n)` — missed last window | Teach `n+1` pattern; double-exclusive concept now understood |
| Kadane's algorithm | Needed full step-by-step trace to unlock it | Always offer a trace first when algorithm feels abstract |
| `zip(*matrix)` | Was new — asked about `*matrix` unpacking | Now internalized — "worth knowing" confirmed |
| Set union `|` operator | Asked "what is `|` here" | Understood quickly once explained |
| `border = (` parenthesis | Thought it was a tuple | Clarified: grouping for line continuation, not a tuple |
| `min(generator)` returns tuple | Expected the value, got `(-freq, num)` | Need `[1]` or unpack — worth a reminder on generator-of-tuples |
| `float('INF')` | Used uppercase — works in Python but non-standard | Nudge toward `float('inf')` lowercase |
| Two solutions / earliest pair | Thought HashMap always returns earliest — it doesn't | Brute force = earliest by (i,j); HashMap = earliest by j |

---

## Mastery Protocol
- Every topic gets a **spaced repeat** — minimum 5–8 problems after first introduction
- When Sean mentions something or asks about it → it goes on the watchpoint list
- Every 10 problems: a **review round** — pick 2–3 from watchpoints and re-probe
- After the test: continue building toward harder variants (Q3/Q4 level consistently)
- Goal: Sean solves any CodeSignal Q1/Q2 in under 5 minutes, Q3 in under 15

---

*Last updated: after 0058 word_search, consolidation mode*
**Mode shift:** exam prep as of 2026-04-18 — focus on speed and confidence over new topics

## Exam Strategy (from recruiter email)
- Q1+Q2 in **under 15 minutes** — string/array/simulation, just pass test cases
- Q3/Q4 medium/hard — if stuck on Q3 for >10 min, **skip to Q4**, come back
- Submit often — check visible test cases early, don't wait until end
- Key topics flagged: **2D arrays/matrices, HashMaps, DSA**
- Sean's additions: deque/BFS, heapq, simulation

## Consolidation Plan (2026-04-19 to test)
Cycle through these — spaced repeats, low-medium difficulty, exam pace:
- HashMap / Counter
- Two pointers
- Sliding window (fixed + variable)
- Kadane's (max/min subarray)
- Binary search
- Prefix sum
- 2D matrix traversal
- Stack
- Simple DP
- Simulation
- Heapq
- BFS / deque
