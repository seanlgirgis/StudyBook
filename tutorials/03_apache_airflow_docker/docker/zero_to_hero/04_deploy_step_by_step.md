# 04 - Deploy Step by Step

Back: [00_START_HERE.md](./00_START_HERE.md)

From this folder:
`D:\Workarea\StudyBook\tutorials\03_apache_airflow_docker\docker`

## Step 1: Prepare env

```powershell
Copy-Item .env.example .env
```

## Step 2: Initialize database + admin user

```powershell
./scripts/manage.ps1 init
```

## Step 3: Start full stack

```powershell
./scripts/manage.ps1 up
```

## Step 4: Validate health

```powershell
./tests/smoke_test.ps1
```

## Step 5: Open UI

- URL: [http://localhost:8088](http://localhost:8088)
- user: `admin`
- pass: `admin`

## Step 6: Trigger first DAG

```powershell
./scripts/newbie_dag.ps1 trigger
```