# Troubleshooting

## Setup checks

- Confirm PostgreSQL is running.
- Confirm the expected database connection values are available.

## SQL file path issues

- Run commands from the intended folder when relative paths are used.
- Confirm copied SQL files exist under the expected practice folder.

## PostgreSQL shell notes

- Use the correct `psql` target database, user, host, and port.
- `\copy` behavior can depend on the current working directory.

## Common query mistakes

- Missing `GROUP BY` columns
- Confusing aggregate and window function behavior
- Forgetting sort direction in ranked outputs
