# migrate_basics.ps1
# Moves all Basics/ notebooks into Language/ DSA/ Advanced_DSA/ DE_Interview/
# Run from: PS D:\Workspace> .\scripts\migrate_basics.ps1
# Safe: skips files already in destination. Never deletes. Runs gitq at end.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$root    = Split-Path $PSScriptRoot -Parent
$basics  = Join-Path $root "Basics"

function Move-NB {
    param([string]$file, [string]$subfolder)
    $src = Join-Path $basics $file
    $dst = Join-Path $basics "$subfolder\$file"
    if (-not (Test-Path $src)) {
        Write-Host "  [?] SKIP — not found : $file" -ForegroundColor DarkYellow
        return
    }
    if (Test-Path $dst) {
        Write-Host "  [=] EXISTS           : $subfolder\$file" -ForegroundColor DarkGray
        return
    }
    Move-Item -Path $src -Destination $dst
    Write-Host "  [>] $file  ->  $subfolder\" -ForegroundColor Green
}

Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  Basics Migration" -ForegroundColor Magenta
Write-Host "  Root: $basics" -ForegroundColor Magenta
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta

# ── LANGUAGE — Python mechanics, not algorithms ──────────────────────
Write-Host ""
Write-Host "[1] Language\" -ForegroundColor White
$language = @(
    "pythonic_idioms_guide.ipynb",
    "dict_comprehensions_guide.ipynb",
    "set_comprehensions_guide.ipynb",
    "generator_expressions_guide.ipynb",
    "lambda_guide.ipynb",
    "sorted_sort_guide.ipynb",
    "map_filter_guide.ipynb",
    "any_all_guide.ipynb",
    "enumerate_zip_guide.ipynb",
    "functools_guide.ipynb",
    "callables_guide.ipynb",
    "unpacking_starred_guide.ipynb",
    "collections_module_guide.ipynb",
    "itertools_guide.ipynb",
    "inner_functions_guide.ipynb",
    "exception_handling_guide.ipynb",
    "type_hints_guide.ipynb",
    "python_internals_guide.ipynb",
    "random_module_guide.ipynb"
)
foreach ($f in $language) { Move-NB $f "Language" }

# ── DSA — Core structures + algorithm patterns ───────────────────────
Write-Host ""
Write-Host "[2] DSA\" -ForegroundColor White
$dsa = @(
    "arrays_master_guide.ipynb",
    "lists_arrays_master_guide.ipynb",
    "multidimensional_tensors_master_guide.ipynb",
    "hashmap_master_guide.ipynb",
    "heap_master_guide.ipynb",
    "linked_list_master_guide.ipynb",
    "string_master_guide.ipynb",
    "stack_master_guide.ipynb",
    "deque_master_guide.ipynb",
    "bit_operations_master_guide.ipynb",
    "binary_search_master_guide.ipynb",
    "sorting_master_guide.ipynb",
    "sorting_algorithms_guide.ipynb",
    "search_algorithms_guide.ipynb",
    "two_pointer_master_guide.ipynb",
    "sliding_window_master_guide.ipynb",
    "prefix_sum_master_guide.ipynb",
    "intervals_master_guide.ipynb",
    "monotonic_stack_master_guide.ipynb",
    "monotonic_deque_master_guide.ipynb"
)
foreach ($f in $dsa) { Move-NB $f "DSA" }

# ── ADVANCED_DSA — Trees, Graphs, DP, Hard patterns ─────────────────
Write-Host ""
Write-Host "[3] Advanced_DSA\" -ForegroundColor White
$advanced = @(
    "binary_tree_master_guide.ipynb",
    "bst_master_guide.ipynb",
    "graphs_bfs_master_guide.ipynb",
    "graphs_dfs_master_guide.ipynb",
    "topological_sort_master_guide.ipynb",
    "union_find_master_guide.ipynb",
    "trie_master_guide.ipynb",
    "dp_1d_master_guide.ipynb",
    "dp_2d_master_guide.ipynb",
    "knapsack_master_guide.ipynb",
    "string_dp_master_guide.ipynb",
    "dp_trees_master_guide.ipynb",
    "backtracking_master_guide.ipynb",
    "segment_tree_master_guide.ipynb",
    "math_number_theory_master_guide.ipynb",
    "greedy_master_guide.ipynb",
    "recursion_guide.ipynb",
    "oop_patterns_guide.ipynb",
    "complexity_reference_guide.ipynb"
)
foreach ($f in $advanced) { Move-NB $f "Advanced_DSA" }

# ── DE_INTERVIEW — System design, SQL, Behavioral ────────────────────
Write-Host ""
Write-Host "[4] DE_Interview\" -ForegroundColor White
$deinterview = @(
    "data_pipeline_design_guide.ipynb",
    "data_warehouse_design_guide.ipynb",
    "distributed_systems_guide.ipynb",
    "stream_processing_guide.ipynb",
    "query_optimization_guide.ipynb",
    "storage_formats_guide.ipynb",
    "cloud_data_platforms_guide.ipynb",
    "orchestration_guide.ipynb",
    "data_quality_guide.ipynb",
    "ml_pipeline_guide.ipynb",
    "sql_window_functions_guide.ipynb",
    "sql_ctes_recursive_guide.ipynb",
    "sql_query_optimization_guide.ipynb",
    "sql_aggregations_guide.ipynb",
    "sql_joins_guide.ipynb",
    "sql_schema_design_guide.ipynb",
    "behavioral_horizonscale_guide.ipynb",
    "behavioral_aws_migration_guide.ipynb",
    "behavioral_telemetry_guide.ipynb",
    "staff_positioning_guide.ipynb",
    "system_design_whiteboard_guide.ipynb"
)
foreach ($f in $deinterview) { Move-NB $f "DE_Interview" }

# ── STAYS AT ROOT — config/reference files ───────────────────────────
Write-Host ""
Write-Host "[5] Root — leaving in place" -ForegroundColor DarkGray
Write-Host "  [=] de_master_curriculum.md" -ForegroundColor DarkGray
Write-Host "  [=] notebook_master_prompt.md" -ForegroundColor DarkGray
Write-Host "  [=] supplementalsINDEX.md" -ForegroundColor DarkGray
Write-Host "  [=] scratchpad.md" -ForegroundColor DarkGray

# ── SUMMARY ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  Migration complete." -ForegroundColor Magenta
$total = $language.Count + $dsa.Count + $advanced.Count + $deinterview.Count
Write-Host "  Files targeted : $total notebooks" -ForegroundColor Yellow
Write-Host "  Subfolders     : Language/ DSA/ Advanced_DSA/ DE_Interview/" -ForegroundColor Yellow
Write-Host "  Root kept      : curriculum + prompts + index files" -ForegroundColor Yellow
Write-Host "══════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

# ── gitq ─────────────────────────────────────────────────────────────
Write-Host "  Running gitq..." -ForegroundColor White
try {
    powershell.exe -Command "gitq"
    Write-Host "  Migration committed." -ForegroundColor Green
} catch {
    Write-Host "  gitq failed — run manually: git add -A && git commit -m 'migrate Basics into subfolders' && git push" -ForegroundColor Red
}
Write-Host ""
