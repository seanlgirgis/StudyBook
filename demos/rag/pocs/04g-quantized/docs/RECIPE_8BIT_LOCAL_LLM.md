# RECIPE - 8-bit Local LLM Container (POC 04g-quantized)

## Scope
This recipe documents the standalone 8-bit local LLM container workflow for `pocs/04g-quantized`.

This is not full RAG. It is a local model-serving proof used for helper tasks.

## Snapshot
- Folder: `D:\Workarea\StudyBook\demos\rag\pocs\04g-quantized`
- Image: `llm_7b_8bit`
- Container: `llm_7b_8bit_run`
- Port mapping: host `8002` -> container `8000`
- Model mount target in container: `/app/llm_model`
- Smoke script: `smoke_test_llm.py` with:
  - `BASE_URL = "http://localhost:8002"`

## Recommended Current Setup
- Active runtime model path on SSD:
  - `C:\LLM_models\Mistral7B`
- Archived duplicate `.bin` weights:
  - `D:\LLM_models\Mistral7B_unused_bin`
- Preferred operating mode:
  - use 8-bit container for day-to-day local helper testing
- FP16 remains a comparison/testing mode only.

## Latest Confirmed Validation (Safetensors Runtime)
- Duplicate `.bin` files were moved out of active C runtime folder and archived on D.
- 8-bit container was recreated with the same C mount (no Docker rebuild).
- Smoke test passed.

Moved files:
- `pytorch_model-00001-of-00002.bin`
- `pytorch_model-00002-of-00002.bin`
- `pytorch_model.bin.index.json`

Archive location:
- `D:\LLM_models\Mistral7B_unused_bin`

Validation run:
```powershell
docker rm -f llm_7b_8bit_run

docker run --gpus all -d -p 8002:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_8bit_run llm_7b_8bit

python .\smoke_test_llm.py
```

Observed result:
- health OK
- inference OK
- PASS reported by smoke script

Observed startup/request logs included:
- `Loading weights: 100%`
- `Application startup complete.`
- `GET /health HTTP/1.1 200 OK`
- `POST /infer HTTP/1.1 200 OK`

Acceptable warning:
- `MatMul8bitLt: inputs will be cast from torch.bfloat16 to float16 during quantization`
- treat as non-fatal if health/infer/smoke tests pass.

## Build (PowerShell)
Run from:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04g-quantized
```

Build image:
```powershell
docker build -t llm_7b_8bit .
```

## Run (C: active model path)
```powershell
docker rm -f llm_7b_8bit_run

docker run --gpus all -d -p 8002:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_8bit_run llm_7b_8bit
```

## Optional Run (D: full model path)
```powershell
docker rm -f llm_7b_8bit_run

docker run --gpus all -d -p 8002:8000 `
  -v D:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_8bit_run llm_7b_8bit
```

## Verify
Health:
```powershell
Invoke-RestMethod http://localhost:8002/health
```

Infer:
```powershell
$response = Invoke-RestMethod http://localhost:8002/infer `
  -Method POST `
  -Body '{ "query": "Explain what an AC repair service does in one short paragraph." }' `
  -ContentType "application/json"

$response.answer
```

Smoke test:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04g-quantized
python .\smoke_test_llm.py
```

Expected smoke condition:
- health returns `{"ok": true}`
- infer returns an `answer`
- script reports PASS

## Operations
Stop 8-bit container:
```powershell
docker stop llm_7b_8bit_run
```

Start existing 8-bit container:
```powershell
docker start llm_7b_8bit_run
```

Remove 8-bit container:
```powershell
docker rm -f llm_7b_8bit_run
```

Tail logs:
```powershell
docker logs -f llm_7b_8bit_run
```

Check GPU from inside container:
```powershell
docker exec -it llm_7b_8bit_run nvidia-smi
```