# OneDriveClean Project Handoff

**Prepared for:** Sean Girgis  
**Project:** OneDriveClean  
**Purpose:** Use local AI, data-engineering workflows, duplicate detection, and safe cloud-to-cloud migration to clean a large OneDrive/photo archive.

---

## 1. Executive Summary

Sean has a large OneDrive archive, roughly **500 GB**, with many files, photos, duplicates, old downloads, unclear folders, and items that may or may not be worth keeping. The goal is not simply to delete files. The goal is to build a safe, repeatable, portfolio-grade cleanup system.

The cleanup system should work like a **data engineering pipeline**:

```text
Messy OneDrive / photos / drives
        ↓
read-only inventory scan
        ↓
hash + metadata + EXIF + file type index
        ↓
duplicate detection
        ↓
photo similarity detection
        ↓
AI classification / tagging
        ↓
human review queue
        ↓
approved copy/migration to clean OneDrive
```

The most important safety principle:

```text
AI recommends. Human approves. The system does not delete automatically.
```

---

## 2. Current PC Diagnostic Summary

The diagnostic report showed that Sean's PC is strong enough to become an AI lab machine.

### Machine

```text
Model: ASUS ROG STRIX G15CF / G15CF
OS: Windows 10 Pro
CPU: Intel Core i7-12700F
Cores: 12 physical cores
Threads: 20 logical processors
RAM: ~64 GB
GPU: NVIDIA GeForce RTX 3060
VRAM: 12 GB
Docker: Installed and running
WSL2: Installed
OneDrive path: D:\Users\shareuser\OneDrive
```

### Storage

```text
C: 512 GB NVMe OS drive
D: 1 TB data drive
F: 1 TB docking/USB drive
E: 14 TB Seagate Expansion drive
```

### Assessment

```text
AI Lab Readiness: GOOD
Recommended setup: Windows host + WSL2 Ubuntu + Docker Desktop + NVIDIA GPU
Do not wipe Windows.
Do not move fully to Linux yet.
Do not buy a second GPU yet.
```

The RTX 3060 12 GB is good for:

```text
7B / 8B local LLMs
some 14B quantized models
CLIP / OpenCLIP image embeddings
photo classification experiments
OCR and metadata workflows
Docker GPU labs
```

It is not ideal for:

```text
large 30B / 70B models
huge vision-language models
large training jobs
massive long-context inference
```

### Docker/WSL observation

Docker currently sees about **31 GB RAM**, even though the machine has about **64 GB**. This is fine for the beginning. Later, if the lab becomes heavier, increase the Docker/WSL memory allocation.

---

## 3. Recommended Operating System Strategy

Do **not** switch to full Linux yet.

Use this:

```text
Windows 10/11 host
  ↓
WSL2 Ubuntu
  ↓
Docker Desktop with WSL2 backend
  ↓
GPU containers / Python / local AI tools
```

Why this is best:

```text
Keeps OneDrive working normally through Windows.
Keeps Windows apps available.
Uses Linux tooling through WSL2.
Allows Docker, Python, CUDA, Ollama, llama.cpp, CLIP, and PyTorch.
Avoids risky driver and OneDrive problems.
```

Full Linux may be useful later only if this PC becomes a dedicated headless server and OneDrive is no longer dependent on the Windows app.

---

## 4. OneDrive Strategy

Sean has:

```text
Source messy OneDrive:
D:\Users\shareuser\OneDrive

Second clean OneDrive:
To be connected separately, ideally through rclone.
```

The best design is hybrid:

```text
Source OneDrive 500 GB
    ↓
direct cloud inventory using rclone
    ↓
folder-by-folder local hydration only when needed
    ↓
local duplicate/photo/AI analysis
    ↓
approved clean output
    ↓
second clean OneDrive
```

Sean has OneDrive configured to **Free up space**, which means not all files are local. This is okay. The workflow should process one folder at a time.

---

## 5. Direct Connection to OneDrive

Yes, we can connect directly to OneDrive without depending only on the Windows OneDrive app.

### Best first option: rclone

Use `rclone` to connect to both OneDrive accounts:

```text
onedrive_dirty = messy/source OneDrive
onedrive_clean = second clean OneDrive
```

rclone can:

```text
list cloud folders
list cloud files
copy selected folders locally
copy approved clean output to the clean OneDrive
compare cloud/local content
run dry-runs before transfer
avoid downloading everything at once
```

Use `copy`, not `sync`, at the beginning.

Important:

```text
rclone sync can delete destination files.
rclone copy is safer for early phases.
```

### Option for later: Microsoft Graph API

Microsoft Graph API can directly access OneDrive items, but it is more complex. Save it for later unless rclone is not enough.

---

## 6. Project Location Decision

Sean chose this code repo location:

```text
D:\Workarea\StudyBook\Proj_development\OneDriveClean
```

This is a good location.

Use this split:

```text
Code repo / GitHub-safe:
D:\Workarea\StudyBook\Proj_development\OneDriveClean

Large local working data / NOT GitHub:
D:\AI_Lab\OneDriveClean

Messy source OneDrive:
D:\Users\shareuser\OneDrive

Second clean OneDrive:
rclone remote: onedrive_clean:
```

The repo should contain:

```text
scripts
src
tests
docs
README
safe examples
config templates
```

The repo should not contain:

```text
real OneDrive files
photos
private documents
large reports
personal inventory databases
logs with personal filenames
rclone tokens
secrets
AI classification output about private files
```

---

## 7. Recommended Local Folder Layout

### GitHub code repo

```text
D:\Workarea\StudyBook\Proj_development\OneDriveClean
  README.md
  .gitignore
  docs\
    DESIGN.md
    SAFETY_RULES.md
    OPERATING_PROCEDURE.md
    DATA_BOUNDARY.md
    TEST_PLAN.md
  scripts\
    setup_lab_folders.ps1
    inventory_rclone_dirty.ps1
    inventory_rclone_clean.ps1
    copy_batch_from_dirty.ps1
  src\
    onedriveclean\
      __init__.py
      inventory_local.py
      reports.py
  tests\
    test_inventory_local.py
  outputs\
    .gitkeep
```

### Local lab data folder

```text
D:\AI_Lab\OneDriveClean
  inventory\
  hydrated\
  analysis\
  reports\
  clean_output\
  quarantine_plan\
  logs\
```

---

## 8. Safety Rules

These are project laws.

```text
No delete in early phases.
No rename in early phases.
No move in early phases.
No sync in early phases.
Copy only.
Dry-run before cloud writes.
AI only recommends.
Human approves.
Source OneDrive is treated as read-only.
Clean OneDrive receives approved copies only.
```

Never start with:

```text
AI auto-delete
full 500 GB download
rclone sync dirty: clean:
full Linux migration
multi-GPU purchase
```

Start with:

```text
inventory
small batch
copy locally
read-only analysis
review report
approved copy to clean OneDrive
```

---

## 9. Recommended `.gitignore`

Create this file:

```text
D:\Workarea\StudyBook\Proj_development\OneDriveClean\.gitignore
```

Suggested content:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
.env

# Local data outputs
data/
outputs/
reports/
logs/
analysis/
hydrated/
clean_output/
quarantine_plan/
inventory/

# Databases / generated indexes
*.sqlite
*.sqlite3
*.db
*.duckdb
*.parquet
*.csv
*.jsonl

# Secrets / credentials
.env
*.env
rclone.conf
.rclone.conf
tokens/
secrets/
credentials/
*.key
*.pem

# Local AI Lab mirror markers
D_AI_Lab_OneDriveClean/
```

---

## 10. DATA_BOUNDARY.md

Create this file:

```text
docs\DATA_BOUNDARY.md
```

Suggested content:

```markdown
# Data Boundary

This repository contains only code, documentation, tests, and safe examples.

Real OneDrive files, personal documents, photos, inventories, reports,
databases, logs, rclone tokens, and AI classification outputs must stay outside
the Git repository.

Local working data belongs under:

D:\AI_Lab\OneDriveClean

The messy source OneDrive is treated as read-only during early phases.

The clean destination OneDrive receives approved copies only after dry-run review.
```

---

## 11. Tooling Recommendations

### Deterministic duplicate/file tools first

Use non-AI first:

```text
SHA256 / BLAKE3 hash
same size + same content
file extension analysis
folder size analysis
EXIF metadata
perceptual photo hash
similar image detection
```

Useful tools:

```text
Czkawka
  Duplicate files, similar images, empty folders, large files.

dupeGuru
  Duplicate finder with picture mode.

ExifTool
  Best tool for image/photo/video metadata.

rclone
  Direct OneDrive/cloud inventory and copy workflows.
```

### Local AI tools later

Use local AI after deterministic scan:

```text
Ollama or llama.cpp
Qwen 7B / 8B / 14B quantized
Mistral 7B
DeepSeek distilled models for reasoning, not bulk tagging
CLIP / OpenCLIP for image embeddings
```

### API use

Cheap API calls should be used only for hard cases:

```text
classify weird files by metadata
summarize folder clusters
name categories
explain duplicate groups
create review reports
```

Do not use API calls for:

```text
all photos
private documents by default
automatic deletion
bulk upload of personal archive
```

---

## 12. Project Phases

### Phase 0 — Read-only cloud inventory

Goal:

```text
Know what exists before touching anything.
```

Outputs:

```text
inventory/onedrive_dirty_files.txt
inventory/onedrive_dirty_top_folders.txt
inventory/onedrive_dirty_total_size.txt
inventory/onedrive_clean_top_folders.txt
inventory/onedrive_clean_total_size.txt
```

### Phase 1 — Local batch copy

Pick one safe folder:

```text
Downloads
Old Downloads
Screenshots
Temp
Phone Backup/Screenshots
Documents/Old
Desktop backup
```

Do not start with family photos.

Copy one folder locally:

```text
onedrive_dirty:<folder>
  ↓
D:\AI_Lab\OneDriveClean\hydrated\batch_001_<name>
```

### Phase 2 — Local deterministic analysis

Reports:

```text
file inventory
extension summary
large files
folder sizes
same filename candidates
exact duplicate groups later
photo metadata later
```

### Phase 3 — AI classification queue

AI receives metadata first, not private file contents by default.

AI categories:

```text
Keep
Archive
Duplicate Review
Photo Review
Likely Junk
Needs Human Review
```

### Phase 4 — Human review and clean output

Create approved clean output:

```text
D:\AI_Lab\OneDriveClean\clean_output\batch_001_<name>
```

### Phase 5 — Copy approved output to clean OneDrive

Use dry-run first.

```text
D:\AI_Lab\OneDriveClean\clean_output\batch_001_<name>
  ↓
rclone copy
  ↓
onedrive_clean:Cleaned/<target>
```

---

## 13. PowerShell Setup Commands

### Create local lab folders

```powershell
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\inventory" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\hydrated" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\analysis" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\reports" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\clean_output" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\AI_Lab\OneDriveClean\logs" | Out-Null
```

### Install rclone

```powershell
winget install Rclone.Rclone
rclone version
```

### Configure OneDrive remotes

```powershell
rclone config
```

Create:

```text
onedrive_dirty
onedrive_clean
```

Both should use storage type:

```text
OneDrive
```

### Test remotes

```powershell
rclone about onedrive_dirty:
rclone about onedrive_clean:

rclone lsd onedrive_dirty:
rclone lsd onedrive_clean:
```

---

## 14. First Inventory Commands

### Dirty OneDrive inventory

```powershell
rclone lsf onedrive_dirty: `
  --recursive `
  --files-only `
  --format "pst" `
  > D:\AI_Lab\OneDriveClean\inventory\onedrive_dirty_files_pst.txt
```

### Dirty top folders

```powershell
rclone lsd onedrive_dirty: `
  > D:\AI_Lab\OneDriveClean\inventory\onedrive_dirty_top_folders.txt
```

### Dirty total size

```powershell
rclone size onedrive_dirty: `
  > D:\AI_Lab\OneDriveClean\inventory\onedrive_dirty_total_size.txt
```

### Clean OneDrive inventory

```powershell
rclone lsd onedrive_clean: `
  > D:\AI_Lab\OneDriveClean\inventory\onedrive_clean_top_folders.txt

rclone size onedrive_clean: `
  > D:\AI_Lab\OneDriveClean\inventory\onedrive_clean_total_size.txt
```

---

## 15. First Batch Copy Example

Recommended first batch:

```text
Downloads
```

If too large, choose:

```text
Downloads\Old
Screenshots
Phone Backup\Screenshots
```

Check size first:

```powershell
rclone size onedrive_dirty:"Downloads"
```

Copy locally:

```powershell
New-Item -ItemType Directory -Force `
  -Path "D:\AI_Lab\OneDriveClean\hydrated\batch_001_downloads" | Out-Null

rclone copy onedrive_dirty:"Downloads" `
  "D:\AI_Lab\OneDriveClean\hydrated\batch_001_downloads" `
  --progress `
  --log-file "D:\AI_Lab\OneDriveClean\logs\batch_001_downloads_copy.log"
```

Use copy, not sync.

---

## 16. Copy Clean Output to Clean OneDrive

Dry-run first:

```powershell
rclone copy `
  "D:\AI_Lab\OneDriveClean\clean_output\batch_001_downloads" `
  onedrive_clean:"Cleaned/Downloads" `
  --dry-run `
  --progress
```

Real copy only after review:

```powershell
rclone copy `
  "D:\AI_Lab\OneDriveClean\clean_output\batch_001_downloads" `
  onedrive_clean:"Cleaned/Downloads" `
  --progress `
  --log-file "D:\AI_Lab\OneDriveClean\logs\batch_001_downloads_to_clean.log"
```

---

## 17. GPU / Docker Validation Commands

### In PowerShell

```powershell
wsl --set-default Ubuntu
wsl -d Ubuntu
```

### Inside Ubuntu/WSL

```bash
nvidia-smi
```

### Test Docker GPU

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

### Test Python CUDA later

```bash
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
    print("vram gb:", torch.cuda.get_device_properties(0).total_memory / 1024**3)
PY
```

---

## 18. GPU Upgrade Guidance

Do not buy a second GPU yet.

First prove the workflow on the RTX 3060 12 GB.

If upgrading later, one larger VRAM GPU is usually better than two smaller GPUs.

Recommended future target:

```text
Used RTX 3090 24 GB
```

Before buying, verify:

```text
power supply wattage, ideally 750W+
case clearance
available PCIe power cables
cooling and airflow
motherboard slot layout
```

Two RTX 3060 cards are less attractive than one 24 GB card for local LLM work.

---

## 19. Codex Prompt 1 — Create Project Foundation

Give this to Codex.

```text
Create a new local project at:

D:\Workarea\StudyBook\Proj_development\OneDriveClean

Purpose:
Build a safe local AI/data-engineering lab for cleaning a large messy OneDrive
and migrating approved clean files into a second clean OneDrive.

Important safety principle:
This project must start as read-only. No source files may be deleted, renamed,
moved, or modified. No rclone sync commands should be generated in phase 1.

Create this structure:

README.md
.gitignore
docs\DESIGN.md
docs\SAFETY_RULES.md
docs\OPERATING_PROCEDURE.md
docs\DATA_BOUNDARY.md
docs\TEST_PLAN.md
scripts\setup_lab_folders.ps1
scripts\inventory_rclone_dirty.ps1
scripts\inventory_rclone_clean.ps1
scripts\copy_batch_from_dirty.ps1
src\onedriveclean\__init__.py
src\onedriveclean\inventory_local.py
src\onedriveclean\reports.py
tests\test_inventory_local.py
outputs\.gitkeep

Requirements:

1. README.md must explain the project in plain English.
2. SAFETY_RULES.md must clearly say:
   - no delete
   - no rename
   - no move
   - no sync
   - copy only
   - dry-run before cloud writes
   - AI only recommends, human approves
3. DATA_BOUNDARY.md must explain that real OneDrive files, inventories,
   personal reports, logs, rclone tokens, and AI outputs stay outside Git.
4. OPERATING_PROCEDURE.md must describe:
   - configure rclone remotes named onedrive_dirty and onedrive_clean
   - inventory dirty OneDrive
   - inventory clean OneDrive
   - choose first batch
   - copy one dirty folder locally
   - analyze locally
   - create clean_output
   - dry-run copy to clean OneDrive
5. setup_lab_folders.ps1 creates:

   D:\AI_Lab\OneDriveClean\inventory
   D:\AI_Lab\OneDriveClean\hydrated
   D:\AI_Lab\OneDriveClean\analysis
   D:\AI_Lab\OneDriveClean\reports
   D:\AI_Lab\OneDriveClean\clean_output
   D:\AI_Lab\OneDriveClean\quarantine_plan
   D:\AI_Lab\OneDriveClean\logs

6. inventory_rclone_dirty.ps1 runs read-only rclone inventory commands
   against onedrive_dirty.
7. inventory_rclone_clean.ps1 runs read-only rclone inventory commands
   against onedrive_clean.
8. copy_batch_from_dirty.ps1 accepts:
   - RemotePath
   - BatchName

   It copies from onedrive_dirty:<RemotePath> into:

   D:\AI_Lab\OneDriveClean\hydrated\<BatchName>

   It must use rclone copy, not sync.
9. inventory_local.py scans a local folder and outputs:
   - path
   - parent folder
   - filename
   - extension
   - size bytes
   - created time
   - modified time
   - guessed category by extension
   - is_photo
   - is_video
   - is_document
10. reports.py creates simple CSV reports:
   - extension summary
   - large files
   - folder sizes
   - same filename candidates
11. Tests must use temporary folders only.
12. .gitignore must exclude local data, reports, logs, databases, tokens,
    csv/jsonl/parquet outputs, rclone config, and secrets.

Do not add AI API calls yet.
Do not add delete/move functionality yet.
Do not add photo similarity yet.
Do not add hash scanning yet unless optional and disabled by default.

At the end, report:
- files created
- how to run setup
- how to configure rclone manually
- how to inventory both OneDrives
- how to copy one batch locally
- how to scan the local batch
- how to run tests
```

---

## 20. Codex Prompt 2 — After Foundation Exists

Use this only after Prompt 1 succeeds.

```text
Continue the OneDriveClean project at:

D:\Workarea\StudyBook\Proj_development\OneDriveClean

Goal:
Add a first read-only local batch scan workflow.

Do not delete, rename, move, sync, or modify source files.
Do not call AI APIs.
Do not process the live OneDrive path directly unless explicitly passed by user.

Add or improve:

1. A PowerShell script:
   scripts\scan_local_batch.ps1

   Parameters:
   - BatchPath
   - BatchName

   It should call the Python inventory/report code and write outputs under:

   D:\AI_Lab\OneDriveClean\reports\<BatchName>

2. Python should produce:
   - file_inventory.csv
   - extension_summary.csv
   - large_files.csv
   - folder_sizes.csv
   - same_filename_candidates.csv

3. Add README examples using:

   D:\AI_Lab\OneDriveClean\hydrated\batch_001_downloads

4. Add tests for report generation using temporary folders only.

5. Update docs\OPERATING_PROCEDURE.md with a simple first-batch walkthrough.

Return:
- files changed
- exact commands to run
- test results
- limitations
```

---

## 21. First Human Workflow After Codex

After Codex creates the project:

```powershell
cd D:\Workarea\StudyBook\Proj_development\OneDriveClean

.\scripts\setup_lab_folders.ps1
```

Configure rclone manually:

```powershell
rclone config
```

Then:

```powershell
.\scripts\inventory_rclone_dirty.ps1
.\scripts\inventory_rclone_clean.ps1
```

Choose first folder:

```powershell
rclone size onedrive_dirty:"Downloads"
```

Copy first batch:

```powershell
.\scripts\copy_batch_from_dirty.ps1 `
  -RemotePath "Downloads" `
  -BatchName "batch_001_downloads"
```

Then scan local batch:

```powershell
.\scripts\scan_local_batch.ps1 `
  -BatchPath "D:\AI_Lab\OneDriveClean\hydrated\batch_001_downloads" `
  -BatchName "batch_001_downloads"
```

---

## 22. Portfolio Story

This project can become a real portfolio story:

```text
Built a local AI-assisted file governance pipeline over a large personal
OneDrive/photo archive. Created cloud inventory, folder-by-folder hydration,
duplicate detection, metadata extraction, photo similarity grouping, AI-assisted
classification, review reports, and human-approved migration into a clean cloud
drive using Python, SQLite/DuckDB, Docker, WSL2, GPU inference, and rclone.
```

Relevant job themes:

```text
data engineering
AI agents
data governance
deduplication
document intelligence
local RAG
privacy-aware AI
cloud migration
metadata pipelines
human-in-the-loop review
```

---

## 23. Final Direction

Start small and safe.

The correct first milestone is:

```text
OneDriveClean v0.1 = read-only rclone inventory + local batch copy + local scan reports
```

Not AI yet.

Not photo similarity yet.

Not delete.

Not sync.

First prove that the pipeline can safely answer:

```text
What files exist?
Where are the largest folders?
What file types dominate?
What folder should be cleaned first?
What exact local batch was copied?
What reports were generated?
```

Once that is stable, move to:

```text
v0.2 exact duplicate detection
v0.3 photo EXIF and image metadata
v0.4 perceptual photo similarity
v0.5 AI-assisted classification queue
v0.6 human review workflow
v0.7 clean OneDrive migration dry-run
```

This is the safe, professional path.
