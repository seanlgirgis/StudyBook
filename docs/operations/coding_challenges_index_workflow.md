# Coding Challenges Index Workflow

This runbook is the canonical guide for managing the coding-challenges index.

## Source of Truth

- Canonical index file: `D:\StudyBook\coding_challenges\index.csv`
- `index.xlsx` is intentionally removed from repository workflow.

## Quick Start

From `D:\StudyBook`:

1. Refresh index from files:
   - `.\refresh_index_and_push.ps1 -SkipGit`
2. Search quickly:
   - `.\search_index.ps1 lc_0238`
3. Open GUI editor:
   - `.\run_index_ui.ps1`

## CLI Commands

Use:
- `.\index_cli.ps1 headers`
- `.\index_cli.ps1 list --limit 20`
- `.\index_cli.ps1 find "anagram" --field title --limit 20`
- `.\index_cli.ps1 show lc_0001`
- `.\index_cli.ps1 open lc_0001 --print-only`

Edit via CLI:
- Add:
  - `.\index_cli.ps1 add --id my_case --path leetcode/by_topic/arrays/my_case.py --set primary=arrays --set tags=arrays;practice --set title="My Case" --set source=leetcode`
- Update:
  - `.\index_cli.ps1 update my_case --set difficulty=medium --set status=in_progress`
- Delete:
  - `.\index_cli.ps1 delete my_case`

## Streamlit GUI Workflow

Launch:
- `.\run_index_ui.ps1`

Then:
1. Use search/filter at top.
2. Click a row in the table (`id`, `title`, `primary`, `tags`) to select it.
3. Click **Edit Selected** to open popup editor.
4. Update any field (all columns are editable in the popup).
5. Click **Apply Changes**.
6. Click **Save CSV** in sidebar to persist to disk.

## Standard Daily Flow

1. `.\refresh_index_and_push.ps1 -SkipGit`
2. Make manual updates via GUI (`.\run_index_ui.ps1`) or CLI (`.\index_cli.ps1 ...`)
3. Save CSV.
4. Run a quick search check (`.\search_index.ps1 <needle>`)
5. Push with your normal git flow.

## Notes

- Streamlit may use `http://localhost:8501` or the next available port.
- If another Streamlit app is running, a different port (for example `8502`) is expected.
