# Apple / Carla PostgreSQL Telemetry Capacity Lab

This lab is for Apple / INSPYR Cloud Capacity interview prep. It is focused on
practical SQL for telemetry, forecasting support, threshold analysis,
capacity risk, and stakeholder-ready reporting.

## Environment
- Container: `sb-postgres`
- Host: `localhost`
- Port: `5432`
- DB: `studybook`
- User: `sb_user`
- Password: `sb_pass_123`
- External psql path: `C:\Program Files\PostgreSQL\17\bin\psql.exe`

## 1) How to Start Docker
```powershell
docker compose -f D:\Workarea\StudyBook\docker\postgres-lab\docker-compose.yml up -d
```

## 2) How to Connect with psql (External Path)
```powershell
$Psql = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'
$env:PGPASSWORD='sb_pass_123'
& $Psql -h localhost -p 5432 -U sb_user -d studybook
```

## 3) How to Run Each SQL File
```powershell
$Psql = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'
$env:PGPASSWORD='sb_pass_123'

& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\01_basic_selects.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\02_joins_and_group_by.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\03_capacity_aggregation.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\04_window_functions.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\05_interview_questions.sql'
```

## 4) Learning Path (Beginner -> Interview)
1. `sql\01_basic_selects.sql`
Begin with table inspection and basic service-level averages.

2. `sql\02_joins_and_group_by.sql`
Practice joins, P95 latency rollups, and daily/hourly aggregations.

3. `sql\03_capacity_aggregation.sql`
Practice threshold breaches, noisy services, forecast-vs-actual, deployment
before/after comparisons.

4. `sql\04_window_functions.sql`
Practice window functions, rankings, moving averages, incident-adjacent metric
views.

5. `sql\05_interview_questions.sql`
Practice interview-style mixed questions with CTEs, scoring, and top-risk lists.

## 5) Apple / Carla Interview Positioning Notes
- Emphasize telemetry-driven capacity decisions, not only dashboarding.
- Speak in terms of P95, headroom, threshold breaches, forecast-vs-actual,
  and risk prioritization.
- Show how SQL outputs drive action: rightsize, scale, investigate, or rebalance.
- Keep claims truthful: strongest hands-on cloud platform is AWS; GCP concepts
  are transferable.
- Clarify finance ownership honestly: technical analytics supports spend
  decisions, without claiming billing-system ownership.

## 6) Exact Reinitialize + Run Commands (PowerShell)
Use this block to refresh the DB with this lab's schema/data and then run all
practice scripts.

```powershell
$Psql = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'
$env:PGPASSWORD='sb_pass_123'

Copy-Item -LiteralPath 'D:\Workarea\StudyBook\playground\prep\init\02_telemetry_schema.sql' -Destination 'D:\Workarea\StudyBook\docker\postgres-lab\init\02_telemetry_schema.sql' -Force
Copy-Item -LiteralPath 'D:\Workarea\StudyBook\playground\prep\init\03_telemetry_seed.sql' -Destination 'D:\Workarea\StudyBook\docker\postgres-lab\init\03_telemetry_seed.sql' -Force

docker compose -f D:\Workarea\StudyBook\docker\postgres-lab\docker-compose.yml down -v
docker compose -f D:\Workarea\StudyBook\docker\postgres-lab\docker-compose.yml up -d

& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\01_basic_selects.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\02_joins_and_group_by.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\03_capacity_aggregation.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\04_window_functions.sql'
& $Psql -h localhost -p 5432 -U sb_user -d studybook -f 'D:\Workarea\StudyBook\playground\prep\sql\05_interview_questions.sql'
```

## Python Side

```powershell
cd D:\Workarea\StudyBook\playground\prep

python scripts\01_smoke_test_db.py
python scripts\02_run_basic_queries.py
python scripts\03_run_capacity_rollups.py
python scripts\04_export_capacity_summary.py

pytest tests -v
```

If connection fails from Windows, try:

```powershell
$env:DB_HOST="localhost"
```
