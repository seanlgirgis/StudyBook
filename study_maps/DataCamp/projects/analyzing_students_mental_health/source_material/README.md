# Source Material

This folder preserves the original source data used by the DataCamp project:

```text
Analyzing Students' Mental Health
```

## Source file

```text
students.csv
```

## Local path

```text
D:\Workarea\StudyBook\study_maps\DataCamp\projects\analyzing_students_mental_health\source_material\students.csv
```

## Dataset summary

```text
Rows: 286
Columns: 50
Local PostgreSQL table: public.students
Database: observability
```

## Important project columns

| Column | Meaning | Project use |
|---|---|---|
| `inter_dom` | International or domestic student | Filter |
| `stay` | Length of stay in years | Grouping |
| `todep` | Depression score | Average PHQ |
| `tosc` | Social connectedness score | Average SCS |
| `toas` | Acculturative stress score | Average AS |

## Header normalization

The original CSV contains a header with a leading space:

```text
 phone
```

The local PostgreSQL table normalizes this to:

```text
phone
```

The remaining columns keep the same source order so `\copy` can load the CSV correctly by position.

## Source handling rules

- Keep the original CSV unchanged.
- Do not edit the raw source file to fix headers or values.
- Normalize field names only in the local table definition.
- Use SQL or documented transformation steps for cleaning.
- Keep derived outputs outside `source_material`.
- Record any future replacement or revised source file in the project audit.

## Load process

The source file is loaded with:

```text
..\lab\sql\01_load_students_csv.sql
```

That script:

1. truncates the local `students` table
2. loads the CSV with `\copy`
3. validates the row count
4. previews the main project columns

Expected row count:

```text
286
```

## Related files

```text
..\lab\sql\00_create_students_table.sql
..\lab\sql\01_load_students_csv.sql
..\lab\sql\02_project_solution.sql
..\study_pages\project_field_guide.html
..\index.html
```

## Provenance note

This CSV is preserved as the project source artifact used to reproduce the DataCamp exercise locally.

The project package should continue to use this file as the canonical local source unless a newer verified version is intentionally adopted and documented.
