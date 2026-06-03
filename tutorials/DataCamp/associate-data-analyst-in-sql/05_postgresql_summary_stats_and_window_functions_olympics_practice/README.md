# Olympics Summer Medals Local Table (Reconstructed)

## Purpose
This folder prepares a local PostgreSQL table that is similar enough to a DataCamp-style `Summer_Medals` table for Course 05 window-function practice.

## Table name
`summer_medals`

## Columns
- `medal_id` (integer, primary key)
- `year` (integer)
- `city` (text)
- `sport` (text)
- `discipline` (text)
- `athlete` (text)
- `country` (text)
- `gender` (text)
- `event` (text)
- `medal` (text)

## Important notes
- This is **not** an official DataCamp export.
- Data seeding will happen later in a separate step.

## How to run later
### DBeaver
1. Open your PostgreSQL connection.
2. Open `01_create_summer_medals_table.sql`.
3. Run the script.

### psql
```powershell
psql -h <host> -p <port> -U <user> -d <database> -f "D:\Workarea\StudyBook\tutorials\DataCamp\associate-data-analyst-in-sql\05_postgresql_summary_stats_and_window_functions_olympics_practice\01_create_summer_medals_table.sql"
```