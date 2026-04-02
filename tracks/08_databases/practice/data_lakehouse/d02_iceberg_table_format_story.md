# Table Formats (Iceberg Concepts) - Story Map

## 1. Story (library catalog)
A library keeps a catalog that lists which shelves hold each book. You read the catalog, not every shelf.

## 2. Core Concepts (street version)
- Metadata file = table definition and current snapshot.
- Manifest = list of data files with partitions.
- Snapshot = versioned view of the table.

## 3. Schema & Partition Evolution
New columns or partitioning rules are recorded in new snapshots without rewriting old data.

## 4. How Queries Work
Engines read metadata + manifests to find the right files and skip the rest.

## 5. Final Mental Model
Iceberg is a catalog of files. Snapshots are versions. Manifests are file lists.

## 6. Run Order
1. c003_iceberg_table_format_demo.py
