# RAG Application Builder Foundation — Field Guide

## Big picture

```text
AI application
= ordinary software
+ model request
+ prompt contract
+ validation
+ monitoring
```

```text
RAG application
= AI application
+ document processing
+ embeddings
+ vector storage
+ retrieval
+ grounded prompt construction
+ source-aware answer
```

## Core component ownership

| Component | Responsibility |
|---|---|
| Local Python | orchestration, files, validation, logging |
| Generation model | produces text or structured output |
| Embedding model | converts text into vectors |
| Vector store | stores and searches vectors |
| Retriever | selects useful context |
| Prompt | defines task, context, and output contract |
| Validator | checks whether output is usable |
| Monitoring | records cost, latency, failures, and quality evidence |

## Learning rule

Never hide a component behind a framework before building and inspecting it
directly.
