
## Completion Flashcards: Pivoting and Totals
- Q: Is CROSSTAB a window function?
  A: No. It is a PostgreSQL pivot/report reshaping tool (`tablefunc`).
- Q: What does ROLLUP add?
  A: Hierarchical subtotal rows (and possibly grand total).
- Q: What does CUBE add?
  A: All subtotal combinations.
- Q: What does COALESCE do in rollup output?
  A: Cleans NULL labels for display; does not create totals.
- Q: Why use ORDER BY inside STRING_AGG?
  A: To preserve intended list order (for example by rank).

- Q: What are CROSSTAB simple query columns?
  A: row identifier, pivot category, cell value.
- Q: NTILE vs percentile_cont?
  A: NTILE labels buckets; percentile_cont computes threshold value.

