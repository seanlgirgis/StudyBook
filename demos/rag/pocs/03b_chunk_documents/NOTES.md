# NOTES (03b_chunk_documents)

- This step intentionally focuses on deterministic chunk preparation only.
- Paragraph-aware splitting improves readability of chunks for humans and debugging.
- Overlap (`100` chars) is included to reduce context loss at chunk boundaries.
- Validation is done at both input (`LoadedDocument`) and output (`DocumentChunk`) levels.
- Inspection note: the first version could split words during overlap, causing broken chunk endings/starts.
- Refinement note: the updated version uses boundary-aware end/start selection so chunks avoid starting or ending in the middle of words when possible.
