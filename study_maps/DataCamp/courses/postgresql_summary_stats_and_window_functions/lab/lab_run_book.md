# Lab Run Book

## Environment

- Date:
- PostgreSQL version:
- Database:
- User:
- `psql` command used:

## Setup evidence

- [ ] Schema created
- [ ] Table created
- [ ] CSV loaded
- [ ] Row count validated as 31,165
- [ ] Distinct year count validated as 27
- [ ] Year range validated as 1896–2012

## Chapter 1 — Window foundations

- [ ] Compared `GROUP BY` with a window aggregate
- [ ] Used `ROW_NUMBER()`
- [ ] Used `ORDER BY` inside `OVER()`
- [ ] Used `PARTITION BY`
- Mistakes and corrections:

## Chapter 2 — Fetching, ranking, and paging

- [ ] Used `LEAD()`
- [ ] Used `FIRST_VALUE()`
- [ ] Used `LAST_VALUE()` with a full frame
- [ ] Used `RANK()`
- [ ] Used `DENSE_RANK()` inside partitions
- [ ] Used `NTILE()`
- [ ] Aggregated results after an `NTILE()` CTE
- Mistakes and corrections:

## Chapter 3 — Aggregate windows and frames

- [ ] Created a running total
- [ ] Created a running maximum
- [ ] Used a bounded moving frame
- [ ] Created a moving average
- [ ] Created a moving total
- [ ] Compared `ROWS` and `RANGE`
- Mistakes and corrections:

## Chapter 4 — Beyond window functions

- [ ] Enabled or reviewed `tablefunc`
- [ ] Created a basic pivot
- [ ] Combined ranking with pivoting
- [ ] Used `ROLLUP`
- [ ] Used `CUBE`
- [ ] Used `COALESCE()`
- [ ] Used `STRING_AGG()`
- Mistakes and corrections:

## Final review

- Strongest topic:
- Topic needing repetition:
- Query worth memorizing:
- Interview explanation to rehearse:
