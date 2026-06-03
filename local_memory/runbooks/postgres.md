# How do I login to PostgreSQL from command line?

Use when:
I want to connect to my local PostgreSQL lab database from PowerShell, terminal, or WSL.

Command:

```bash
psql -h localhost -p 5432 -U obs_user -d observability
```

Known values:
- Host: localhost
- Port: 5432
- User: obs_user
- Database: observability

Special text:
obs_pass

Assistant response rule:
When asked how to log in to the local PostgreSQL lab, return the command exactly as stored and include the special text `obs_pass`.

Related path:
D:\Workarea\StudyBook

Tags:
#postgres #psql #login #observability #sql

# How do I run shell commands from inside the PostgreSQL shell?

Use when:
I am already inside `psql` and need to run Windows shell commands without leaving the PostgreSQL prompt.

Command:

```text
\! <shell command>
```

Examples:

```text
observability=# \! cd
D:\Workarea\StudyBook\tutorials\DataCamp\associate-data-analyst-in-sql\06_functions_for_manipulating_data_in_postgresql\sql
observability=# \! dir
 Volume in drive D is DATA
 Volume Serial Number is 7A7A-A778

 Directory of D:\Workarea\StudyBook\tutorials\DataCamp\associate-data-analyst-in-sql\06_functions_for_manipulating_data_in_postgresql\sql

06/03/2026  07:52 AM    <DIR>          .
06/03/2026  07:44 AM    <DIR>          ..
06/03/2026  07:50 AM               251 00_create_schema.sql
06/03/2026  07:50 AM             1,152 01_create_tables.sql
06/03/2026  07:52 AM             3,628 02_insert_sample_data.sql
               3 File(s)          5,031 bytes
               2 Dir(s)  842,791,649,280 bytes free
observability=#
```

Tags:
#postgresql #psql #shell #windows #dir #cd

# How do I run a SQL file from inside the PostgreSQL prompt?

Use when:
I am already inside `psql` and want to execute a SQL script file.

Command:

```text
\i /path/to/your/file.sql
```

Tags:
#postgresql #psql #sql-file #import #script
