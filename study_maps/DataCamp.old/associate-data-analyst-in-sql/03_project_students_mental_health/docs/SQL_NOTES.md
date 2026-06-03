# SQL Notes

## Suggested Workflow
1. Load data with Python loader.
2. Run `sql/02_explore_table.sql` to validate assumptions.
3. Run `sql/03_project_solution.sql` for final project output.

## Focus Areas
- `inter_dom` separates international and domestic students.
- `stay` is central for trend analysis by duration.
- `todep`, `tosc`, `toas` are aggregate targets in the final query.

## Quality Checks
- Confirm row count after loading.
- Confirm `inter_dom` contains expected values.
- Check nulls before interpreting averages.
