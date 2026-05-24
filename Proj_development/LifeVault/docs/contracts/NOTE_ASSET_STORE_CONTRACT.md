# NOTE_ASSET_STORE_CONTRACT.md

## Purpose

Define global note asset store rules for SUC_005 notes/images/assets.

## Global Asset Store Root

- `D:\AI_Lab\LifeVault\notes_assets\`

## Core Rules

1. Assets are deduplicated across all LifeVault notes by SHA.
2. Same SHA reuses existing asset.
3. Original filename is metadata only (not canonical identity).
4. Hint/story metadata may be attached to asset references.
5. Asset store is append-only by default.
6. No normal delete/update/rename operations in v0.
7. Large image warnings are allowed; note-friendly derivatives may be added later.

## Identity Model

- canonical key: content hash (SHA)
- storage naming: content-addressed
- reference model: note links to asset key + display metadata

## Portability Rules

- note retrieval/export packages should materialize required assets under `assets/`
- markdown links in package remain relative

## Deferred Items

- encryption for sensitive assets
- derivative generation pipeline
- retention/deletion policy beyond append-only default
