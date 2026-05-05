# TEST PLAN - POC 04g Local LLM Container

## Objective
Verify that the standalone local LLM container can be built, started with GPU and mounted model files, and can answer through `/health` and `/infer`.

## Preconditions
- Windows machine with Docker Desktop running
- NVIDIA GPU available (observed: RTX 3060, 12 GB VRAM)
- model files present at `C:\LLM_models\Mistral7B`
- working directory:
  - `D:\Workarea\StudyBook\demos\rag\pocs\04g\llm`

## Test 1 - Build Image
Command:
```powershell
docker build -t llm_7b_offline .
```

Expected result:
- build completes successfully
- image `llm_7b_offline` available

## Test 2 - Run Container With GPU + Mounted Model
Command:
```powershell
docker run --gpus all -d -p 8000:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_run llm_7b_offline
```

Expected result:
- container starts in detached mode
- `docker ps` shows `llm_7b_run`

## Test 3 - Health Endpoint
Command:
```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected result:
```json
{"ok": true}
```

## Test 4 - Inference Endpoint
Command:
```powershell
$response = Invoke-RestMethod http://localhost:8000/infer `
  -Method POST `
  -Body '{ "query": "Hello. Explain what an AC repair service does in one short paragraph." }' `
  -ContentType "application/json"

$response.answer
```

Expected result:
- non-empty answer string is returned
- answer quality is acceptable for a local prototype smoke check

## Test 5 - Scripted Smoke Test
Command:
```powershell
python .\smoke_test_llm.py
```

Expected PASS signal:
- script prints health output with `"ok": true`
- script prints inference output containing `"answer"`
- final line includes:
  - `PASS: LLM container responded successfully.`

## Container Log Confirmation (Supporting)
Command:
```powershell
docker logs -f llm_7b_run
```

Expected indicators observed:
- CUDA runtime banner
- Uvicorn startup on `0.0.0.0:8000`
- model weight loading reaches `100%`
- startup complete

## Known Limitations (Not Test Failures)
- response latency can be slow
- responses can occasionally over-generate and continue beyond desired stopping point
- partial CPU offload can occur on 12 GB VRAM hardware

## Pass/Fail Rule For This POC Slice
PASS when all are true:
- image builds
- container starts with GPU and mounted model
- `/health` responds correctly
- `/infer` returns answer text
- smoke test script reports PASS