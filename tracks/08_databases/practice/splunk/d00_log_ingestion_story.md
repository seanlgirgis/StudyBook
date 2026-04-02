# Log Ingestion and Indexing Concepts - Story Map

## 1. Story (mail sorting)
Letters arrive as raw text. The mailroom reads the address, sorts them into bins, and stores them for quick lookup.

## 2. Core Concepts (street version)
- Ingestion = bring raw logs into Splunk.
- Parsing = extract fields from raw text.
- Indexing = store events in an index for fast search.

## 3. What Happens
Raw logs are ingested, fields like service or level are parsed, and events are placed into an index.

## 4. Search Concept
Queries filter on indexed fields like `level=ERROR` to find issues quickly.

## 5. Final Mental Model
Splunk turns raw logs into searchable events by parsing and indexing.

## 6. Run Order
1. c001_log_ingestion_demo.py
