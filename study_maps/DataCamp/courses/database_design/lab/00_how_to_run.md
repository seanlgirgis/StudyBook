# How to Run

From PowerShell:

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design\lab
psql -U postgres -d studybook -f .\sql\00_reset_schema.sql
psql -U postgres -d studybook -f .\sql\01_operational_schema.sql
psql -U postgres -d studybook -f .\sql\02_seed_operational_data.sql
psql -U postgres -d studybook -f .\sql\03_analytical_schema.sql
psql -U postgres -d studybook -f .\sql\04_views_roles_partitioning.sql
psql -U postgres -d studybook -f .\sql\05_validation_queries.sql
```

Use a different database name or role if your local PostgreSQL environment requires it.
