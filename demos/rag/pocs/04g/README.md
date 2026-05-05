# POC 04g - Local LLM Container Setup (Standalone)

## Purpose
POC 04g documents a standalone local LLM container baseline on Sean's Windows machine.

Goal proven in this slice:
- run a local 7B-class LLM container with Docker + NVIDIA GPU support
- mount local Mistral model files from SSD into the container
- expose a FastAPI API
- verify successful responses from `/health` and `/infer`

This is a containerized local-LLM infrastructure proof, not full RAG integration yet.

## What Was Proven
The following were completed and tested successfully:
- Docker image build from `nvidia/cuda:13.0.1-runtime-ubuntu22.04`
- container runtime with `--gpus all` on NVIDIA RTX 3060 (12 GB VRAM)
- model mount from `C:\LLM_models\Mistral7B` to `/app/llm_model`
- FastAPI app startup in container (`uvicorn` on port `8000`)
- endpoint checks:
  - `GET /health` returns `{"ok": true}`
  - `POST /infer` returns a generated answer string
- local smoke script execution: `python .\smoke_test_llm.py` returned PASS

## How 04g Differs From 04f
- `04f` remains the prior standalone local RAG/fuzzy/intent demo lane.
- `04g` is the newer local-LLM/container lane focused first on standing up the model-serving runtime.
- `04g` intentionally defers knowledge-base retrieval integration.

## Current Status
- Status: PASS for standalone local LLM container smoke test.
- Scope status: complete for this narrow infrastructure proof.

## Current Limitations
- Response latency can be slow.
- Generation can occasionally overrun into extra text/follow-up style output.
- Container logs indicate some model parameters offloaded to CPU/RAM due to VRAM limits; this is acceptable for this prototype but impacts speed.

## Environment Snapshot
- Host OS: Windows
- Python env used locally: `proj_educate`
- Docker Desktop: reinstalled and working
- Docker data path configured: `D:\DokerData\DockerDesktopWSL`
- GPU: NVIDIA RTX 3060, 12 GB VRAM

## Model Files
Model directory used:
- `C:\LLM_models\Mistral7B`

Observed model folder contents include both safetensors and PyTorch `.bin` shards plus tokenizer/config files. The app loads from `MODEL_PATH` and the directory is mounted at `/app/llm_model`.

## Repro Steps (PowerShell)
Run from:
- `D:\Workarea\StudyBook\demos\rag\pocs\04g\llm`

Build image:
```powershell
docker build -t llm_7b_offline .
```

Remove old container if present:
```powershell
docker rm -f llm_7b_run
```

Run container with GPU and mounted model directory:
```powershell
docker run --gpus all -d -p 8000:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_run llm_7b_offline
```

Inspect container state/logs:
```powershell
docker ps
docker logs -f llm_7b_run
```

Health test:
```powershell
Invoke-RestMethod http://localhost:8000/health
```

Inference test:
```powershell
$response = Invoke-RestMethod http://localhost:8000/infer `
  -Method POST `
  -Body '{ "query": "Hello. Explain what an AC repair service does in one short paragraph." }' `
  -ContentType "application/json"

$response.answer
```

Smoke test:
```powershell
python .\smoke_test_llm.py
```

## Build Lessons Captured
- Early apt failures were tied to intermittent network/packet-loss issues to `archive.ubuntu.com`.
- Docker network check used:
  - `docker run --rm busybox ping -c 4 archive.ubuntu.com`
- Offline `.deb` install attempt under `llm/debs/` was not the final successful path.
- Final successful build used `apt-get` after Docker/network stability recovered.
- PyTorch wheel index should be used only for torch packages; API/model libraries should be installed from normal PyPI.

## Non-Goals For This Slice
- No full RAG pipeline in 04g yet
- No KB retrieval integration yet
- No move into `integrated/servicecall-ai`
- No production-readiness claim