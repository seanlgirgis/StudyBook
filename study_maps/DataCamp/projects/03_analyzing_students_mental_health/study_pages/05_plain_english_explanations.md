## Local PostgreSQL SQL Analysis Ladder - First Pass

### Inspect the table
Start by viewing sample rows and counting total rows. This confirms the table loaded and gives a quick feel for the data shape.

### Check data quality
Run missing-value checks on key analysis columns (`inter_dom`, `stay`, `todep`, `tosc`, `toas`). If many values are null, averages and group comparisons can be misleading.

### Understand categories
Count category values like `inter_dom` and `academic`. This shows how data is distributed across groups and whether some groups are very small.

### Compare groups
Compute average `todep`, `tosc`, and `toas` by `inter_dom` to compare domestic vs international patterns at a high level.

### Analyze length of stay
Aggregate averages by `stay`, then focus on `inter_dom = 'Inter'` to study international students specifically across different stay durations.

### Produce the final project query
Finish with the grouped international-only query sorted by `stay DESC`, returning count and three rounded averages (`average_phq`, `average_scs`, `average_as`).
