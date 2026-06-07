# Troubleshooting

- Run scripts in numeric order.
- Use a role allowed to create schemas and roles.
- If `CREATE ROLE` fails because the role exists, use `DROP ROLE database_design_analyst;` only when safe, or skip role creation.
- The seeded dates and partitions are intentionally fixed for repeatable practice.
- `EXPLAIN` output varies by PostgreSQL version and statistics.
