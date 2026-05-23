# How to Run Course 11 PySpark Labs in Docker

Purpose:
Explain how to enter the Docker PySpark shell, move around the mounted
StudyBook filesystem, inspect lab files, and run Python lab scripts.

## 1. Start from Windows PowerShell

Command:

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
```

Explain:
This initializes the StudyBook shell. The DataCamp project uses the StudyBook
root bootstrap.

## 2. Enter the Docker shell

Command:

```powershell
docker exec -it sharkforce-pyspark-lab bash
```

Explain each part:
- docker = use Docker
- exec = run a command inside an already-running container
- -it = interactive terminal
- sharkforce-pyspark-lab = container name
- bash = Linux shell inside the container

Show prompt change:

Windows:
`(proj_educate) PS D:\Workarea\StudyBook>`

Docker:
`root@sharkforce-pyspark-lab:/workspace#`

## 3. Understand the mounted filesystem

Explain:

Windows path:
`D:\Workarea\StudyBook`

Docker path:
`/workspace/studybook`

Meaning:
Windows owns the files. Docker provides the PySpark runtime. The bind mount
connects them.

Bind mount:

`D:/Workarea/StudyBook:/workspace/studybook`

## 4. Move to the lab root

Command:

```bash
cd /workspace/studybook/tutorials/DataCamp/Associate_Data_Engineer_Databricks/course_11_intro_pyspark
pwd
ls
```

Explain:
`pwd` shows the current folder.
`ls` lists files and folders.

## 5. Inspect code from the shell

Commands:

```bash
cat 03_missing_data_and_columns/lab_missing_data_and_columns.py
head -n 40 03_missing_data_and_columns/lab_missing_data_and_columns.py
tail -n 40 03_missing_data_and_columns/lab_missing_data_and_columns.py
grep "SparkSession" 01_sparksession_dataframe_basics/lab_sparksession_dataframe_basics.py
grep -R "broadcast" .
```

Explain:
- `cat` shows the whole file
- `head` shows the top of the file
- `tail` shows the bottom
- `grep` searches text
- `less`/`more` may not exist in this minimal container

## 6. Run one lab from the lab root

Examples:

```bash
python 01_sparksession_dataframe_basics/lab_sparksession_dataframe_basics.py
python 02_reading_data_and_schemas/lab_reading_data_and_schemas.py
python 03_missing_data_and_columns/lab_missing_data_and_columns.py
```

Explain:
`python` runs the script using Docker's Python/PySpark runtime.

## 7. Run labs one by one

```bash
python 01_sparksession_dataframe_basics/lab_sparksession_dataframe_basics.py
python 02_reading_data_and_schemas/lab_reading_data_and_schemas.py
python 03_missing_data_and_columns/lab_missing_data_and_columns.py
python 04_filtering_and_aggregations/lab_filtering_and_aggregations.py
python 05_joins_and_unions/lab_joins_and_unions.py
python 06_udfs_and_pandas_udfs/lab_udfs_and_pandas_udfs.py
python 07_rdds_vs_dataframes/lab_rdds_vs_dataframes.py
python 08_spark_sql_temp_views/lab_spark_sql_temp_views.py
python 09_scale_explain_cache_broadcast/lab_scale_explain_cache_broadcast.py
python 10_production_support_checks/lab_production_support_checks.py
```

## 8. Exit Docker shell

Command:

```bash
exit
```

Explain:
This returns to Windows PowerShell.

## 9. Common warning

Common warning:

`WARN NativeCodeLoader: Unable to load native-hadoop library...`

Explain:
This is usually safe for the local Docker learning labs. Spark falls back to
built-in Java classes. It is a warning, not a lab failure.

## 10. Tiny memory hook

Windows owns the files.
Docker owns the runtime.
The mount connects them.
`python lab.py` runs the lab.
