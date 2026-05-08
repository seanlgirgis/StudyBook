# RUNBOOK.md

## PowerShell
```powershell
cd D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab
docker compose build --no-cache
docker compose up
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
docker exec -it sharkforce-pyspark-lab bash
```

## Inside Container
```bash
java -version
python --version
python -c "import pyspark; print(pyspark.__version__)"
```

## Jupyter
`http://localhost:8888/lab`