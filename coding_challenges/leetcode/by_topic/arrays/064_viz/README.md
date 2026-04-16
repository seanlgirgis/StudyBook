# LC 64 — Minimum Path Sum · DP Visualizer

Interactive step-by-step visualization of the dynamic programming solution for [LeetCode 64](https://leetcode.com/problems/minimum-path-sum/).

## How to Run

**Option A — Claude Code preview (recommended)**
Open a Claude Code session in this repo and say:
> "Start the dp-viz preview"

Claude will call `preview_start → dp-viz` using the `.claude/launch.json` config and open it in the built-in browser.

**Option B — Plain browser (no server needed)**
Just open the file directly:
```
coding_challenges/leetcode/by_topic/arrays/064_viz/index.html
```
Double-click it in Explorer or drag it into any browser. No build step, no dependencies.

**Option C — Python one-liner**
```bash
python -m http.server 7432 --directory coding_challenges/leetcode/by_topic/arrays/064_viz
# then open http://localhost:7432
```

---

## How to Use

| Control | What it does |
|---------|-------------|
| **Preset buttons** (top) | Switch between 6 different grids — including a greedy trap |
| **Next / Prev** | Step forward or backward one cell at a time |
| **▶ Auto** | Plays through all steps at ~1 step/sec; click again to pause |
| **↺ Reset** | Restart the current grid from step 0 |

### Reading the display

```
ORIGINAL GRID          DP TABLE (running min-cost)
┌───┬───┬───┐          ┌───┬───┬───┐
│ 1 │ 3 │ 1 │          │ 1 │ 4 │ 5 │
├───┼───┼───┤          ├───┼───┼───┤
│ 1 │ 5 │ 1 │    →     │ 2 │ 7 │ 6 │
├───┼───┼───┤          ├───┼───┼───┤
│ 4 │ 2 │ 1 │          │ 6 │ 8 │ 7 │
└───┴───┴───┘          └───┴───┴───┘
```

- **Purple cell** — cell currently being computed
- **Arrow (↓ or →)** — which neighbor the value came from
- **Small top-right number** — original grid value for that cell
- **Large number** — minimum cost to reach this cell from (0, 0)
- **Green cells** — optimal path, shown after the final step

### The three DP rules

```
(0,0)          →  dp = grid[0][0]              # start
top row        →  dp[0][c] = dp[0][c-1] + grid[0][c]     # only from left
left column    →  dp[r][0] = dp[r-1][0] + grid[r][0]     # only from above
everything else→  dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c]
```

---

## Presets

| Name | Grid | Answer | What it demonstrates |
|------|------|--------|----------------------|
| 3×3 Standard | `[[1,3,1],[1,5,1],[4,2,1]]` | 7 | Classic LeetCode example |
| 2×3 Rectangle | `[[1,2,3],[4,5,6]]` | 12 | Non-square grid |
| Greedy Trap | `[[1,9,1],[1,9,1],[1,1,1]]` | 5 | Right column looks tempting; optimal path hugs left then bottom |
| Tall 3×2 | `[[1,2],[1,1],[4,1]]` | 4 | More rows than columns |
| 1×1 | `[[5]]` | 5 | Trivial base case |
| Single Row | `[[1,2,5]]` | 8 | Only right moves possible |

---

*Visualizer: plain HTML/CSS/JS — no frameworks, no build step.*
