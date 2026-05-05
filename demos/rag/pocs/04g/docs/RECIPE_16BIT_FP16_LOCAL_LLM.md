# RECIPE - 16-bit (FP16) Local LLM Container (POC 04g)

## Scope
This recipe documents the standalone FP16 local LLM container workflow for `pocs/04g`.

This is not full RAG. It is a local model-serving proof only.

## Snapshot
- Folder: `D:\Workarea\StudyBook\demos\rag\pocs\04g\llm`
- Image: `llm_7b_offline`
- Container: `llm_7b_run`
- Port mapping: host `8000` -> container `8000`
- Model mount target in container: `/app/llm_model`

## Why Use This Recipe
Use this mode when explicitly validating the FP16 container path.

Known limitation:
- On RTX 3060 (12 GB VRAM), FP16 Mistral 7B can trigger CPU/RAM offload and slower response times.

Observed warning during FP16 operation:
- `Some parameters are on the meta device because they were offloaded to the cpu.`

## Build (PowerShell)
Run from:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04g\llm
```

Build image:
```powershell
docker build -t llm_7b_offline .
```

## Run (C: model path)
```powershell
docker rm -f llm_7b_run

docker run --gpus all -d -p 8000:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_run llm_7b_offline
```

## Run (D: model path)
```powershell
docker rm -f llm_7b_run

docker run --gpus all -d -p 8000:8000 `
  -v D:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_run llm_7b_offline
```

## Verify
Container list:
```powershell
docker ps
```

Logs:
```powershell
docker logs -f llm_7b_run
```

Health:
```powershell
Invoke-RestMethod http://localhost:8000/health
```

Infer:
```powershell
$response = Invoke-RestMethod http://localhost:8000/infer `
  -Method POST `
  -Body '{ "query": "Explain what an AC repair service does in one short paragraph." }' `
  -ContentType "application/json"

$response.answer
```

## Operational Commands
Stop:
```powershell
docker stop llm_7b_run
```

Start existing:
```powershell
docker start llm_7b_run
```

Remove:
```powershell
docker rm -f llm_7b_run
```

## Practical Guidance
- Keep FP16 container stopped unless explicitly testing FP16 behavior.
- Prefer 8-bit mode for regular local helper workloads.