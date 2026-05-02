# ChatGPT RAG Context — ServiceCall AI

## Demo Name

ServiceCall AI / RAG Demo Workspace

## Local Path

`D:\Workarea\StudyBook\demos\rag`

## Purpose

ServiceCall AI is a learning-first RAG demo for a home-services business.

The goal is to build an AI intake and knowledge assistant that can eventually:

- live inside a business website
- answer from business documents
- cite sources
- collect service-intake details
- ask clarification when intent is unclear
- escalate risky cases
- log outcomes
- later run through FastAPI, Docker, ECS Fargate, CI/CD, and CloudWatch

## Business Theme

Synthetic company:

`North Texas Comfort & Home Services`

Focus:

- A/C repair
- A/C replacement
- heating repair
- maintenance plans
- plumbing
- water heaters
- appliance repair

All business data is synthetic demo data.

## Project Strategy

Two lanes:

- `pocs/` — small learning proof-of-concepts
- `integrated/servicecall-ai/` — final assembled demo later

Rule:

Nothing moves into `integrated/servicecall-ai/` until it is understood in `pocs/`.

## Completed

- Project shell and control files exist
- Static website shell exists
- Chat widget placeholder exists
- Cloudflare static smoke test worked
- Synthetic business documents exist
- Retrieval ladder is staged
- `03a_load_documents` is implemented and tested

## Current Active Step

Next step:

`03b_chunk_documents`

Goal:

Take loaded documents from `03a_load_documents` and split them into smaller searchable chunks with metadata.

Do not jump to TF-IDF yet.

## Current Learning Ladder

- `03a_load_documents` — done
- `03b_chunk_documents` — next
- `03c_text_normalization`
- `03d_word_tfidf_index`
- `03e_char_tfidf_typo_search`
- `03f_hybrid_retrieval`
- `03g_retrieval_decision`
- `03h_retrieval_evaluation`

## Environment Rule

Before Python, pytest, pip, FastAPI, or project scripts:

```powershell
. D:\Workarea\StudyBook\env_setter.ps1