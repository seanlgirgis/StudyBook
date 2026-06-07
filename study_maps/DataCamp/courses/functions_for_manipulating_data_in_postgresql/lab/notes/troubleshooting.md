# Troubleshooting

- `permission denied to create extension`: skip the optional extension block or use a database role with the required privilege.
- `operator does not exist` for arrays: confirm both sides have compatible array element types.
- unexpected text parsing results: inspect `POSITION()` first and handle zero before calculating boundaries.
- timestamp arithmetic confusion: use `pg_typeof(expression)` to inspect the result type.
- script path failure in psql: start psql from the canonical course directory or use an absolute `\i` path.
