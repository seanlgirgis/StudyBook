# Troubleshooting

## `psql` is not recognized

Add the PostgreSQL `bin` directory to `PATH`, or call `psql.exe` with its full path.

Example:

```powershell
& 'C:\Program Files\PostgreSQL\17\bin\psql.exe' -U postgres -d studybook
```

## Password prompt appears repeatedly

Set the `PGPASSWORD` environment variable temporarily:

```powershell
$env:PGPASSWORD = 'your-password'
```

Clear it afterward:

```powershell
Remove-Item Env:PGPASSWORD
```

A `.pgpass` file is safer for repeated use.

## `\copy` cannot find `summer.csv`

Run the setup command from the lab root. The load script expects:

```text
.\data\summer.csv
```

Check:

```powershell
Test-Path .\data\summer.csv
```

## Database does not exist

Create it first:

```powershell
createdb -U postgres studybook
```

Or use another existing database with the `-Database` parameter.

## Permission denied for `CREATE EXTENSION`

`tablefunc` may require a role with sufficient privileges. All other lab sections can still be completed.

Ask an administrator to run:

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
```

## Objects cannot be found

Confirm the scripts use:

```sql
SET search_path TO dc_window_lab, public;
```

Or qualify the table:

```sql
dc_window_lab.summer_medals
```

## Running total crosses country boundaries

Add:

```sql
PARTITION BY country
```

inside `OVER()`.

## LAST_VALUE repeats the current value

Use a frame ending at:

```sql
UNBOUNDED FOLLOWING
```

## CROSSTAB output is misaligned

Ensure the source query is ordered by:

```text
row key, category
```

and that the declared output columns match the category values.
