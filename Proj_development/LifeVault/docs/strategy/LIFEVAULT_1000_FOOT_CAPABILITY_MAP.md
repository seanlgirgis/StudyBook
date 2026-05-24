# LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md

## 1. LifeVault Definition

LifeVault is a personal AI-assisted vault for files, folders, notes, note folders/books, URLs/URIs, images/photos/screenshots/scans, code folders/projects, binary/archive/install files, media, contacts, emails/mbox imports/attachments, physical items and physical containers, job/career records, prompts and AI agent configuration, tasks/projects/maintenance queues, and secret references/sensitive notes, with searchable metadata, user stories, lifecycle status, storage tracking, and guided workflows.

Core principle:

Everything important becomes or relates to a `vault_item`.

## 2. Core Spine

`capture -> classify -> store -> search -> review -> publish -> verify -> cleanup`

The current local folder lifecycle has already proven this spine end-to-end in v0.

## 3. Major Item Types LifeVault May Store

- local folders
- individual files
- text-capable documents
- binary files
- installers
- archives/zips
- images/photos/screenshots/scans
- media/music/video
- URLs/URIs/bookmarks
- notes
- note folders/books
- prompts
- AI agent configs
- code folders/projects
- job-search records
- personal important files
- secret references and encrypted secret files later
- backup/export bundles
- people/project/event records if needed
- contacts
- emails/mbox imports/attachments
- physical items and physical containers
- tasks/projects/maintenance queues
- note folders/books

## 4. Cross-Cutting Capabilities

- multi-destination final storage
- multi-copy tracking
- system-managed final storage
- user stories attached to any item
- hot/warm/cold/archive/quarantine lifecycle status
- metadata search
- content search when approved
- image/OCR search later
- duplicate detection
- sensitivity classification
- encryption/decryption future layer
- backup/restore
- multi-machine portability
- Streamlit control center
- AI/Codex skill orchestration
- contacts/people vault operations
- email and attachment vault operations
- task/project/maintenance queue management

## 5. Revised Super-Use-Case List

- SUC_001 Universal Capture / Ingest
- SUC_002 Classification, Story, Tags, and Lifecycle
- SUC_003 Storage Location and Multi-Copy Management
- SUC_004 Search, Retrieve, Hydrate, and Open
- SUC_005 Notes and Knowledge Memory
- SUC_006 File and Folder Lifecycle
- SUC_007 Images, Scans, OCR, and Visual Memory
- SUC_008 Code and Project Archive
- SUC_009 Binary and Media Archive
- SUC_010 Secrets and Sensitive Records
- SUC_011 Job, Career, and Document Records
- SUC_012 AI Prompts, Agent Skills, and Config Memory
- SUC_013 Backup, Restore, Portability, and Multi-Machine
- SUC_014 Encryption, Decryption, and Secure View
- SUC_015 Streamlit Control Center / Agent Console
- SUC_016 Reporting, Audit, and Governance
- SUC_017 Cleanup, Retention, and Space Recovery
- SUC_018 Physical Storage Inventory
- SUC_019 Contacts and People Vault
- SUC_020 Email and Attachment Vault
- SUC_021 Tasks, Projects, and Maintenance Queues

## 6. Cyclical Development Strategy

- do not spend months perfecting one lane
- build thin slices across major item types
- persistent storage early gives value
- GUI/control center should start early as guide/search display
- scripts/Python carry execution load
- AI/agent layer guides and reasons
- encryption is important but can be layered in cycles

## 7. First Suggested Development Cycles

### Cycle 1

- finish SUC_001 v0 local folder lifecycle
- add broad capability map
- add hot/cold field planning
- add note item design
- add URL item design
- add simple task/maintenance queue v0 design
- start Streamlit read-only dashboard

Current note status:

- SUC_005 note v0 design contracts completed
- implementation remains future cycle work

### Cycle 2

- implement notes v0
- implement URL/bookmark v0
- improve search/retrieve
- add hot/warm/cold status

### Cycle 3

- image/media inventory v0
- code folder ingestion v0
- binary archive v0

### Cycle 4

- OneDrive/cloud storage tracking
- encryption/decryption design
- secure view

## 8. Open Questions

- What is final storage policy?
- What gets copied vs moved?
- What is hot by default?
- Which items can be stored plaintext?
- What belongs in LifeVault vs a password manager?
- What should the Streamlit control center show first?
- What belongs in LifeVault vs a password manager?
