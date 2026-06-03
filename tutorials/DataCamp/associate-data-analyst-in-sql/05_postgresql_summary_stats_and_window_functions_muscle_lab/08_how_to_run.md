# How to Run (PostgreSQL)

## psql style
```powershell
psql -h <host> -p <port> -U <username> -d <database_name> -f "00_create_schema.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "01_create_tables.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "02_seed_sales_events.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "03_seed_employee_sales.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "04_seed_server_telemetry.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "05_seed_olympic_medals_practice.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "06_seed_support_tickets.sql"
psql -h <host> -p <port> -U <username> -d <database_name> -f "07_validation_queries.sql"
```

## DBeaver style
1. Open your PostgreSQL connection (`host`, `port`, `database_name`, `username`).
2. Open SQL Editor in this folder.
3. Run files in order:
   - `00_create_schema.sql`
   - `01_create_tables.sql`
   - `02_seed_sales_events.sql`
   - `03_seed_employee_sales.sql`
   - `04_seed_server_telemetry.sql`
   - `05_seed_olympic_medals_practice.sql`
   - `06_seed_support_tickets.sql`
   - `07_validation_queries.sql`

## Reminder
All objects are under schema:
`course05_muscle`
