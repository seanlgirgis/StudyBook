# What This Teaches

## Documents On Disk Are Not Yet Retrieval-Ready
Raw markdown files are useful source material, but retrieval systems need structured objects with consistent metadata before indexing or scoring.

## Why Pydantic Models Help
Pydantic enforces required fields and simple data-quality rules early, so malformed source records fail fast instead of creating hidden downstream retrieval bugs.

## Why Metadata Matters
Fields like `source_file`, `source_path`, `character_count`, and `line_count` improve traceability, debugging, and later citation behavior.

## How This Becomes Input For Chunking
`SourceDocument` records from this stage are the direct input for `03b_chunk_documents`, where each full document is split into smaller chunk units with chunk-level metadata.
