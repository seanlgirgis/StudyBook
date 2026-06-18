# LifeVault → Grok Build Handoff

**Target save path:** `D:\Workarea\StudyBook\Proj_development\LifeVault\docs\handoffs\CHATGPT_GROK_HANDOFF_2026-06-17.md`  
**Authoring role:** ChatGPT as LifeVault architect  
**Audience:** Sean, Grok Director, Codex implementer  
**Date:** 2026-06-17

## 1. Role Boundaries: ChatGPT vs Codex vs Grok

**ChatGPT — Architect layer**
- Owns product architecture, data model reasoning, safety rules, tradeoff analysis, and long-term design coherence.
- Helps Sean decide what LifeVault should become before implementation details harden too early.
- Produces handoffs, architectural rules, prompt contracts, naming strategy, and review criteria.

**Codex — Implementer layer**
- Writes code, edits repository files, creates tests, runs validations, and follows scoped task prompts.
- Should not make major product, security, data-retention, or architecture decisions on its own.
- Must ask for architectural clarification when requirements conflict or touch sensitive storage, privacy, encryption, or deletion.

**Grok Director — Future guardian / build director**
- Takes ownership of `GROK_*` agent files and operational build coordination.
- Converts Sean’s intent plus architect decisions into staged implementation tasks for Codex.
- Should protect the architecture from drift, scope creep, unsafe automation, and agent overreach.

## 2. Product Vision — 1000-foot View

- LifeVault is a private personal vault for documents, notes, assets, contacts, emails, attachments, tasks, projects, physical inventory, and future searchable “life stories.”
- The core value is not just storage; it is AI-assisted digestion into future-ready metadata, summaries, stories, sensitivity labels, and search hooks.
- The system should support deduplication across the whole vault, not just inside one folder, note, or document package.
- LifeVault should treat item type as a controlled managed list, while still allowing new types to be added as the product evolves.
- The design must support local-first privacy, masking, encryption, selective AI use, and cheap commercial AI where safe and cost-effective.

## 3. Done vs Planned vs Deferred

**DONE / strongly established**
- LifeVault concept and direction are clear: private vault + AI digestion + search-ready stories.
- Core vault item categories were identified: individual documents, notes/assets, contacts, emails/attachments, tasks/projects, and physical storage inventory.
- Deduplication principle established: assets/images/files should dedupe globally across LifeVault.
- `vault_item_type` should be controlled/managed, not random free text.
- Tasks are accepted as a `vault_item_type`; projects contain task groups; task groups contain tasks.
- Each task should optionally support an editable Markdown notes file that can be reprocessed.
- Same-folder/package duplicates should usually be cleaned because duplicate files with different names in the same package are rarely useful.

**PLANNED / likely next architecture work**
- Define canonical vault item schema and controlled type registry.
- Define ingestion pipeline: file discovery → fingerprinting → sensitivity scan → text extraction → masking → AI story generation → metadata writeback.
- Define storage layout for original files, extracted text, generated stories, thumbnails/assets, and indexes.
- Define agent boundaries for Grok Director, Codex implementer, and any future local automation.
- Compare AI providers and prompts for “best story” quality, cost, and safety before batch processing.

**DEFERRED / not first build**
- Full local GPU-heavy AI processing for everything.
- Batch AI processing at scale before prompts and schemas stabilize.
- Complex UI polish before vault model, ingestion, dedup, and safety contracts are proven.
- Fully autonomous cleanup/deletion.
- Deep enterprise-grade document management features unless Sean explicitly asks.

## 4. Top 5 Design Decisions Driven by ChatGPT

1. **AI digestion matters more than basic search.**  
   Rationale: If LifeVault writes strong stories, summaries, entities, and metadata up front, future search becomes easier and more meaningful.

2. **Use controlled `vault_item_type`, not free text.**  
   Rationale: This keeps routing, search, UI, prompts, and validation stable while still allowing the list to evolve.

3. **Deduplicate globally.**  
   Rationale: Notes, assets, emails, and documents will reuse the same files/images; global fingerprinting prevents waste and confusion.

4. **Separate file format from vault type.**  
   Rationale: PDF, DOCX, JPG, and XLSX are formats/attributes, not necessarily the meaning of the item. A deed can be PDF or image; the vault item type is “deed/document,” not “PDF.”

5. **Start with API-based AI testing, batch later.**  
   Rationale: Sean needs to compare providers, prompt quality, safety behavior, and cost before committing to large-scale processing.

## 5. Top 5 Open Questions / Parking Lot

1. What is the first minimum lovable LifeVault slice: documents only, OneDrive cleanup, notes/assets, or task/project vault?
2. What exact schema should define a `vault_item`, and which fields are required vs optional?
3. How should sensitivity scanning and masking work before any content is sent to commercial AI?
4. Should original files remain in source locations, be copied into a vault store, or both?
5. What is the right split between LifeVault, `local_memory`, and Markdown runbooks?

## 6. Safety Laws to Always Enforce with Sean

- Never delete, overwrite, or “clean up” originals without explicit approval and a tested backup path.
- Never send sensitive documents, IDs, banking data, medical data, passwords, or private identifiers to external AI without masking and explicit approval.
- Never assume AI-generated stories are facts; preserve source links and confidence boundaries.
- Never let Codex or another agent silently change architecture, retention, encryption, or deletion behavior.
- Always favor reversible steps, logs, dry runs, manifests, and human review before destructive operations.
- Keep secrets out of repo files, prompts, logs, handoffs, and generated documentation.

## 7. ChatGPT-only Conversations / Decisions Sean May Export Separately

Known relevant ChatGPT conversation threads include:

- **2026-05-21 — OneDrive File Classification AI**: AI lab PC diagnostics, OneDrive cleanup direction, local vs cloud access, and early project setup thinking.
- **2026-05-22 — Startup Codex for OneDriveClean**: Codex workflow, dedup rules, contacts/email/storage/task expansion, Markdown notes for tasks, and LifeVault typed-item design.
- **2026-05-28 — LifeVault Design Ideas**: document types, AI story strategy, extraction vs sending files, provider testing, masking, sensitivity detection, API-first processing.
- **2026-06-01 — RTX 3060 for Local RAG**: GPU feasibility, cheaper commercial GenAI as bridge, local RAG privacy tradeoffs, masking/encryption strategy.

Sean should export these chats if Grok needs fuller historical context.

## 8. Merge / Decommission Opinion

**Recommendation: keep LifeVault standalone for now.**

LifeVault is becoming a product/system, not just a memory folder. It needs its own schema, ingestion pipeline, dedup engine, safety policies, and storage rules. Do not merge it too early into `local_memory`, because that could blur personal memory, file vaulting, and operational runbooks.

Best split:
- **LifeVault:** canonical vault data, documents, assets, stories, metadata, dedup, indexes, safety policy.
- **local_memory:** lightweight assistant/project memory and reusable context summaries.
- **Markdown runbooks:** human-readable operating procedures, install notes, recovery steps, and agent instructions.

Later, LifeVault can expose selected summaries into `local_memory`, but `local_memory` should not become the vault itself.

## 9. What Grok Must NEVER Do Without Explicit Approval

- Never delete, move, rename, archive, or deduplicate real user files automatically.
- Never process a large folder tree against paid AI without a cost cap and Sean’s approval.
- Never send unmasked sensitive content to external AI providers.
- Never change encryption, backup, retention, or source-of-truth rules silently.
- Never convert controlled type fields into uncontrolled free text.
- Never let Codex invent schema-breaking shortcuts just to make code pass quickly.
- Never store secrets, API keys, credentials, tokens, or private IDs in repo-tracked files.
- Never treat generated AI metadata as legally reliable or source-of-truth evidence.
- Never collapse LifeVault into another project until Sean approves the architectural split.
