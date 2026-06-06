# PostgreSQL Summary Stats and Window Functions Field Guide

## Course map

1. Window-function foundations
2. Fetching and ranking
3. Aggregate windows and frames
4. Supporting analytical SQL techniques

## Core mental model

A window function calculates across related rows while preserving one result row for every input row.

## Essential pattern

```sql
function_expression OVER (
    PARTITION BY grouping_column
    ORDER BY ordering_column
    ROWS BETWEEN frame_start AND frame_end
)
```

## Chapter links

- [Chapter 1](chapter_01_introduction_to_window_functions_field_guide.html)
- [Chapter 2](chapter_02_fetching_ranking_and_paging_field_guide.html)
- [Chapter 3](chapter_03_aggregate_window_functions_and_frames_field_guide.html)
- [Chapter 4](chapter_04_beyond_window_functions_field_guide.html)
- [SQL Quick Lookup](sql_quick_lookup.html)
- [Lab Run Book](../lab/lab_run_book.md)

## Reusable interview sentence

Window functions let me calculate rankings, comparisons, running totals, and moving statistics across related rows without collapsing the detailed result set as `GROUP BY` would.
