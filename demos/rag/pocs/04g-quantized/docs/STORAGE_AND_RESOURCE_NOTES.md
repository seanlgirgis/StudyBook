# STORAGE AND RESOURCE NOTES (POC 04g / 04g-quantized)

## Scope
Practical storage and resource notes for local Mistral 7B container testing on Windows.

This is standalone local LLM container work, not full RAG.

## Recommended Current Setup (Validated)
- Keep active safetensors runtime model on C SSD:
  - `C:\LLM_models\Mistral7B`
- Archive duplicate PyTorch `.bin` weights on D (backup, not deleted):
  - `D:\LLM_models\Mistral7B_unused_bin`
- Use 8-bit container for day-to-day local helper testing.
- Keep FP16 mode as documented comparison/testing only.

## Latest Confirmed Validation
Moved out of active runtime folder (`C:\LLM_models\Mistral7B`):
- `pytorch_model-00001-of-00002.bin`
- `pytorch_model-00002-of-00002.bin`
- `pytorch_model.bin.index.json`

Archived to:
- `D:\LLM_models\Mistral7B_unused_bin`

After move, 8-bit container was restarted with the same C mount and passed smoke test.

Run used:
```powershell
docker rm -f llm_7b_8bit_run

docker run --gpus all -d -p 8002:8000 `
  -v C:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_8bit_run llm_7b_8bit

python .\smoke_test_llm.py
```

Observed smoke PASS output included:
- health check OK
- inference answer returned
- `PASS: LLM container responded successfully.`

Observed logs included:
- `Loading weights: 100%`
- `Application startup complete.`
- `GET /health HTTP/1.1 200 OK`
- `POST /infer HTTP/1.1 200 OK`

## What This Confirms
- For the current 8-bit container setup, PyTorch `.bin` files are not required at runtime.
- Safetensors + tokenizer/config files are sufficient for the current mounted model folder.
- No Docker image rebuild was required after moving `.bin` files.
- Container recreate/restart was sufficient because model files are mounted at runtime.

## Acceptable Non-Fatal Warning
Observed warning:
- `MatMul8bitLt: inputs will be cast from torch.bfloat16 to float16 during quantization`

Interpretation:
- acceptable for this current setup
- non-fatal when health/infer endpoints and smoke test pass

## Model Directory and File Format Notes
Active runtime model path:
- `C:\LLM_models\Mistral7B`

Historical storage note:
- safetensors shards are about 14.5 GB
- PyTorch `.bin` shards are about 15 GB
- keeping both formats duplicates storage footprint

Current practice:
- keep safetensors-based active runtime set on C
- keep `.bin` set archived on D as fallback backup

## Resource Behavior Notes
### FP16 (`pocs/04g`)
- Works, but slower on RTX 3060 (12 GB VRAM).
- Observed warning indicates CPU/RAM offload:
  - `Some parameters are on the meta device because they were offloaded to the cpu.`
- Result: higher latency and heavier system pressure.

### 8-bit (`pocs/04g-quantized`)
- Worked better in local testing.
- Faster responses observed.
- No CPU-offload warning observed in successful runs.
- Current preferred local mode for helper workloads.

## Optional: Full Model Relocation to D Drive
This remains optional and can be used if you want to run the active model from D.

Potential target:
- `D:\LLM_models\Mistral7B`

Recommended safe process:
1. Create destination folder.
2. Copy model files.
3. Run 8-bit container using D-drive mount.
4. Run smoke test.
5. Only after successful test, optionally remove old C copy.

Commands:
```powershell
mkdir D:\LLM_models\Mistral7B
robocopy C:\LLM_models\Mistral7B D:\LLM_models\Mistral7B /E

docker rm -f llm_7b_8bit_run

docker run --gpus all -d -p 8002:8000 `
  -v D:\LLM_models\Mistral7B:/app/llm_model `
  --name llm_7b_8bit_run llm_7b_8bit

cd D:\Workarea\StudyBook\demos\rag\pocs\04g-quantized
python .\smoke_test_llm.py
```