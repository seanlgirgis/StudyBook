# Troubleshooting

## `\copy` cannot find the CSV

Confirm that `lab/data/summer.csv` exists. Re-run the bootstrap script with `-SourceCsv` if needed.

## Permission denied for `CREATE EXTENSION`

Run the extension command as a PostgreSQL role with sufficient privileges, or skip the optional CROSSTAB exercise.

## Schema objects are not found

Run `00_create_schema.sql` and `01_create_tables.sql` first, and confirm the active database.
