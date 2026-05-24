# SUC_005_ACCEPTANCE_CHECKLIST.md

## SUC_005 Acceptance Checklist (Design + v0 Progress)

- [ ] Note can be represented as a `vault_item` (`vault_item_type=note`).
- [x] Note has a physical markdown file with generated safe filename.
- [x] Note can be edited outside LifeVault.
- [ ] LifeVault reindex expectation is documented for metadata/body.
- [ ] Note folder can group notes and apply shared policy.
- [ ] Asset duplicate SHA reuse rule is defined.
- [ ] Portable note package contract works with relative links.
- [ ] Sensitive note `public_hint` remains searchable.
- [ ] `encrypted_body` behavior is deferred and explicitly non-implemented in this phase.
- [x] Filename is generated automatically by default.
- [ ] Title can change without renaming the physical file.
- [ ] Template is tracked (`template_id`).
- [ ] Template version is recorded.
- [x] User filename override is sanitized.
- [x] No overwrite by default for note filename creation.

Notes v0 thin-slice checks:

- [x] Create note CLI/wrapper works with `notes_root`.
- [x] Search notes CLI/wrapper supports title/story/tags/body match.
- [x] Temp-path tests cover note creation and search behavior.
- [ ] Older notes remain valid after template updates.
