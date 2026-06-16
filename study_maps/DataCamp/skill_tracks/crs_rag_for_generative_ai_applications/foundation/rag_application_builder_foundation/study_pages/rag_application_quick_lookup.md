# RAG Application Quick Lookup

## Application flow

```text
input → validate → prompt → model → parse → validate → output
```

## RAG flow

```text
documents
→ extract
→ clean
→ chunk
→ embed
→ store

question
→ embed
→ retrieve
→ build grounded prompt
→ generate
→ cite
```

## Embedding rule

Document embeddings and query embeddings for one index must use a compatible
embedding model and vector space.

## Budget rule

```text
local configured budget
-
locally tracked estimated cost
=
estimated local remaining budget
```

This is not the same as the provider account's actual remaining credit.
