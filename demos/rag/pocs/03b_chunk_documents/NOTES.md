# NOTES (03b_chunk_documents)

- This step intentionally focuses on deterministic chunk preparation only.
- Paragraph-aware splitting improves readability of chunks for humans and debugging.
- Overlap (`100` chars) is included to reduce context loss at chunk boundaries.
- Validation is done at both input (`LoadedDocument`) and output (`DocumentChunk`) levels.
