# DESIGN - POC 04g Local LLM Container Setup

## Problem Statement
POC 04g validates that a standalone local LLM service can run on a Windows machine with Docker and NVIDIA GPU support before attempting full RAG integration.

## Scope
In scope:
- standalone FastAPI model-serving container
- local GPU runtime via Docker `--gpus all`
- mounted local Mistral model files from SSD
- endpoint-level proof through `/health` and `/infer`

Out of scope:
- retrieval-augmented generation pipeline
- knowledge-base retrieval integration
- movement into `integrated/servicecall-ai`

## Architecture
High-level flow:
- User request -> FastAPI app in Docker container -> local mounted Mistral model -> generated response

Concrete mount/runtime path:
- host model path: `C:\LLM_models\Mistral7B`
- container model path: `/app/llm_model`
- app load path in code: `MODEL_PATH = "./llm_model"`

## Runtime Design
Base image:
- `nvidia/cuda:13.0.1-runtime-ubuntu22.04`

Build design:
- install `python3`, `python3-pip`, `git` through `apt-get`
- install PyTorch packages from the CUDA wheel index
- install FastAPI/Uvicorn/Transformers stack from normal PyPI

Run design:
- publish `8000:8000`
- run with `--gpus all`
- mount local model directory into `/app/llm_model`

## Why 04g Is Separate From RAG Integration
04g isolates one question: can a local containerized 7B-class model be reliably built, started, and called on this PC?

Keeping this separate from retrieval and orchestration reduces ambiguity during troubleshooting:
- container/runtime issues can be debugged independently
- model-loading and GPU behavior can be verified before adding KB retrieval complexity

## Why KB Is Not Integrated Yet
KB integration is intentionally deferred because this slice targets infrastructure proof only:
- prove container + model loading + API endpoints first
- preserve a clean baseline before adding retrieval paths

## Performance Notes
Observed runtime behavior includes:
- container logs show model loads successfully
- logs also indicate partial CPU offload for some parameters

Interpretation:
- with RTX 3060 (12 GB VRAM), the model may not reside fully in VRAM
- partial CPU/RAM offload is acceptable for prototype success criteria
- tradeoff is slower response latency

## Design Lessons Captured
- intermittent network connectivity to `archive.ubuntu.com` blocked early apt installs
- offline `.deb` path was attempted but not final success path
- after Docker/network stabilization, standard `apt-get` flow became reliable
- package index separation matters:
  - PyTorch from PyTorch CUDA wheel index
  - non-torch packages from normal PyPI