# Troubleshooting

## Setup checks

- Confirm PostgreSQL is running.
- Confirm connection environment variables are set if defaults are not used.

## Common SQL load issues

- Schema recreation may fail if permissions are restricted.
- `\copy` usage depends on the shell and working directory.

## CSV path issues

- Confirm the CSV exists at `data/raw/students.csv`.
- If the filename changes, update the command or rename the file locally.

## PostgreSQL shell notes

- Use the correct database, user, and port.
- Run SQL files from the project root when relative paths matter.
