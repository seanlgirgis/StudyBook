# Course 11 Map Group-Filter Usability Fix

## Problem Observed
In `outputs/course_11_intro_pyspark_1000ft.html`, group filtering worked functionally, but selected groups did not stand out strongly enough for study. Non-selected nodes dimmed only lightly, and active-state emphasis was subtle.

## Root Cause Found
Shared StudyBubble viewer behavior (not topic data) had weak visual contrast for filtered states:
- Group filter logic was correctly applying visibility.
- Non-selected node opacity and link contrast were not strong enough for learning focus.
- Active filter button styling did not provide a strong enough visual "selected" signal.

## Files Changed
- `Study_bubbles/viewer/bubble_viewer.css`
- `Study_bubbles/viewer/bubble_viewer.js`

## Fix Type
Mixed CSS + JS (shared viewer behavior).

## What Changed
- Strengthened active group button style (clearer border/glow/weight).
- Added explicit filtered-state classes for links:
  - `.is-filter-match`
  - `.is-filter-dim`
- Added explicit filtered-state class for nodes:
  - `.is-filter-match`
- Updated filter application logic to:
  - keep selected-group nodes fully visible and highlighted,
  - make non-selected nodes more subdued during group filter,
  - keep selected-group links clearly visible,
  - strongly dim non-selected links.

## Behavior After Fix
When a group filter is active:
- Active group button is clearly visible.
- Selected-group nodes stay bright/readable with stronger outline.
- Selected-group links stay visibly present.
- Non-selected nodes and links are subdued.
- `All` and `Reset` restore full normal visibility.

## Maps Rebuilt
- `outputs/course_11_intro_pyspark_1000ft.html`
- `outputs/course_11_intro_pyspark_architecture_runtime.html`

## Manual Browser Test Instructions
1. Open: `outputs/course_11_intro_pyspark_1000ft.html`
2. Click group filters in this order:
   - `Architecture`
   - `DataFrame Work`
   - `Execution Model`
   - `Production`
   - `All`
   - `Reset View`
3. Expected:
   - selected group is visually obvious,
   - non-selected groups are strongly subdued,
   - `All`/`Reset` restore normal map visibility.
