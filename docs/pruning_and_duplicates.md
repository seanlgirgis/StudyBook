# StudyBook — Pruning & Duplicates Analysis

**Date:** 2026-04-27
**Purpose:** Identify what can be cleaned up, deduplicated, or removed to keep the repo lean and navigable.

---

## Summary

**Pruning performed: 2026-04-27 — committed to main**

| Category | Count | Status | Action Taken |
|----------|-------|--------|-------------|
| Binary files tracked in git (`index.xlsx`) | 1 | ✅ Done | `git rm --cached` — gitignore already present |
| Windows shortcut files (`StudyBook.lnk`, `temp.lnk`) | 2 | ✅ Done | `git rm --cached`, added `*.lnk` to .gitignore |
| `__dupNNN` files in legacy prompts | 88 | ✅ Done | All 88 verified had originals — deleted, LOOP-023 closed |
| Temp migration artifact run folders | 3 | ✅ Done | Deleted `run_20260402_*` folders from `temp/migration_meta/` |
| `coding_challenges/_archive/` | 2 folders | ✅ Done | Deleted (workspace_legacy + cleaning_gc superseded) |
| Tutorial `02_pyspark` number collision | 1 | ✅ Done | Renamed → `48_pyspark_local`, refs updated in `_manager/` |
| `.docx` binaries in `data/jobs/` | 217 | ✅ Done | `git rm --cached` all, added `data/jobs/**/*.docx` to .gitignore |
| `prompt_READY_TO_PASTE.md` copies | 46 | ✅ Keep | Intentional per-tutorial — topic-specific content |
| MongoDB credential in `.env.local` (LOOP-007) | 1 | ⏳ Open | Requires passphrase + Atlas rotation — owner action needed |
| `HorizonScale/` scope clarification | — | ⏳ Open | Decide: own repo vs keep in StudyBook |
| `jobdatabrain-tagger/` scope clarification | — | ⏳ Open | Decide: own repo vs keep in StudyBook |

---

## 1. Binary Files Tracked in Git

### `coding_challenges/index.xlsx`
- **Problem:** Binary Excel file is committed to git. Caused push rejection due to file size (LOOP-089). Workflow was migrated to CSV-first (`index.csv`) in LOOP-090.
- **Status:** `index.xlsx` is still tracked (`git ls-files` confirms).
- **Action:** Remove from git tracking. The CSV is the source of truth.
```powershell
git rm --cached coding_challenges/index.xlsx
# Add to .gitignore: coding_challenges/index.xlsx
git commit -m "remove stale index.xlsx binary from tracking — CSV is source of truth"
```

### `coding_challenges/StudyBook.lnk`
- **Problem:** Windows shortcut file committed to git. Meaningless outside this machine. Causes unnecessary noise in git history.
- **Action:** Remove from tracking.
```powershell
git rm --cached "coding_challenges/StudyBook.lnk"
# Add to .gitignore: *.lnk
git commit -m "remove Windows shortcut file from git tracking"
```

---

## 2. `__dupNNN` Files in Legacy Prompts (88 files)

**Location:** `_prompts/legacy/technologies/R1/`, `R2/`, `R3/`

**Cause:** During migration wave M-011/M-013 (2026-04-02), files with matching names in source and destination were conflict-safe duplicated with a `__dupNNN` suffix rather than overwriting. This is documented in LOOP-023 (open).

**Evidence file:** `temp/migration_meta/run_20260402_121903/conflicts_report.md`

**Examples found:**
```
T1-A1_kafka_intro__dup001.md
T1-A2_kafka_concepts__dup001.md
T1-B1_spark_intro__dup001.md
... (88 total)
```

**Action:** Compare each `__dupNNN` file against its non-dup counterpart. In most cases the dup is an older version of the same content — safe to delete.

```powershell
# Find all dup files
Get-ChildItem -Recurse -Path "_prompts\legacy" -Filter "*__dup*" | Select-Object FullName

# For each, diff against original:
# diff "T1-A1_kafka_intro.md" "T1-A1_kafka_intro__dup001.md"
# If identical or older version → delete the __dup file
```

**Risk:** Low — these are legacy prompts already superseded by canonical tracks. Worst case: recover from git history.

---

## 3. `prompt_READY_TO_PASTE.md` Copies (46 files)

**Location:** `tutorials/<each_tutorial_folder>/prompt_READY_TO_PASTE.md`

**Cause:** Intentional design — each tutorial has a localized AI context prompt specific to that topic so agents working in that subdirectory have immediate context without reading the full repo.

**Decision: KEEP — do not deduplicate.**

Each file contains topic-specific content, not identical boilerplate. They are structurally duplicated by design.

**Minor cleanup:** Audit that the content of each file actually differs from a generic template. If any are empty or contain only boilerplate with no topic-specific content, replace with a symlink or a reference to a shared template.

---

## 4. `.docx` Binaries in `data/jobs/` (217 files)

**Location:** `data/jobs/<uuid>/` — 65 job application folders, each containing:
- `raw_intake.md`
- `metadata.yaml`
- `resume.docx`
- `cover.docx`

**Problem:** 217 `.docx` files are binary blobs committed to git. They grow unboundedly with every new job application (~3.3 docx per job). These bloat clone size and push times without adding searchable content.

**Options (pick one):**

| Option | Effort | Effect |
|--------|--------|--------|
| **A. Gitignore `.docx` in `data/jobs/`** | Low | New jobs won't track docx; old ones remain |
| **B. Remove old jobs from tracking (keep recent 10)** | Medium | Reduces history bloat |
| **C. Archive old job folders to S3 / local archive** | Medium | Clean git, full retention elsewhere |
| **D. Status quo** | None | Continues to grow |

**Recommended action (Option A + B):**
```powershell
# 1. Add to .gitignore
Add-Content .gitignore "`ndata/jobs/**/*.docx"

# 2. Remove all tracked docx from git index (keeps files on disk)
git ls-files data/jobs/**/*.docx | ForEach-Object { git rm --cached $_ }

# 3. Commit
git commit -m "stop tracking job application docx binaries — files kept locally"
```

---

## 5. Windows Shortcut Files

| File | Location | Action |
|------|----------|--------|
| `StudyBook.lnk` | `coding_challenges/` | Remove from git (see §1) |
| `Home.lnk` | `HorizonScale/` | Check if tracked; if so, remove |
| `temp.lnk` | `temp/` | Check if tracked; if so, remove |

**Global fix:** Add `*.lnk` to `.gitignore` to prevent future shortcut files from entering the repo.

```
# .gitignore addition
*.lnk
```

---

## 6. Temp Migration Artifacts

**Location:** `temp/migration_meta/`

| Run folder | Date | Status |
|------------|------|--------|
| `run_20260402_121841` | 2026-04-02 | Migration complete — artifacts likely safe to delete |
| `run_20260402_121903` | 2026-04-02 | Migration complete — `conflicts_report.md` still needed for LOOP-023 |
| `run_20260402_122601` | 2026-04-02 | Migration complete — likely safe to delete |

**Action:** After resolving LOOP-023 (`__dupNNN` cleanup), delete all `temp/migration_meta/` run folders. The emergency rollback backups are at `C:\Users\shareuser\migration_backups\` (not in git).

**Also check:** `temp/airflow_lab/` — Airflow lab temp artifacts. Review if still needed.

---

## 7. Duplicate-Numbered Tutorial Folders

| Folder | Content | Issue |
|--------|---------|-------|
| `tutorials/02_pyspark/` | Local PySpark (no Docker) — 5 lesson files | Number `02` conflicts |
| `tutorials/02_PySpark_Docker/` | Docker Spark cluster — 7 validated lessons | Number `02` conflicts |

**Both are distinct and valid.** The number collision just makes ordering confusing.

**Action:** Renumber `02_pyspark` → `02b_pyspark_local` or `48_pyspark_local` (next available number).
```powershell
Rename-Item tutorials\02_pyspark tutorials\48_pyspark_local
# Update any references to the old path in prompt_READY_TO_PASTE.md etc.
```

---

## 8. `coding_challenges/_archive/`

**Contents:**
- `cleaning_gc_2026-04-10/` — garbage collection cleanup from April 10
- `workspace_legacy/` — legacy Workspace content before migration

**Action:** Review contents. If all migrated and verified, delete. These are safe to remove since the migration evidence is stored in `temp/migration_meta/` and the backups are at `C:\Users\shareuser\migration_backups\`.

---

## 9. `HorizonScale/` at Repo Root

**Observation:** `HorizonScale/` sits at the StudyBook repo root but appears to be its own sub-project (has own `env_setter.ps1`, `models/`, `data/`, `config/`). It includes an `Anna Course` folder and `legacy/` subfolder.

**Question:** Is this intentionally inside StudyBook or should it be its own sibling repo?

**Action:** Clarify scope. If it's Sean's forecasting project, it may belong as `D:\Workarea\HorizonStudy` (which already exists as a separate repo). If it's study material about forecasting, keep here under `tracks/` instead.

---

## 10. `jobdatabrain-tagger/` at Repo Root

A job tagging POC with its own `env_setter.ps1`, database, data sources. Has real substance — background DB updater, dictionary extraction.

**Decision needed:** Is this a standalone project (should be its own repo) or study material (keep in StudyBook)? Given it has a database and env_setter, it may deserve its own `D:\Workarea\jobdatabrain-tagger` repo.

---

## 11. Known Open Secrets Issue

**LOOP-007 (open):** MongoDB credentials are still in `_infra/env/.env.local` as plaintext (gitignored, but not yet migrated into the encrypted secrets system).

**Action:**
```powershell
.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "MONGODB_URI"
# Then remove from .env.local and rotate the Atlas password
```

---

## Priority Order

| Priority | Item | Effort | Payoff |
|----------|------|--------|--------|
| 1 | Remove `index.xlsx` + `StudyBook.lnk` from git tracking | 10 min | Cleaner git, no push risk |
| 2 | Gitignore `*.lnk` and `data/jobs/**/*.docx` | 15 min | Stop future bloat |
| 3 | Resolve LOOP-023: review 88 `__dupNNN` files | 30 min | Remove confirmed redundant files |
| 4 | Delete `temp/migration_meta/` after LOOP-023 closes | 5 min | Tidy temp folder |
| 5 | Renumber `02_pyspark` → `48_pyspark_local` | 5 min | Fix ordering confusion |
| 6 | Resolve LOOP-007: MongoDB secret rotation | 20 min | Closes a security gap |
| 7 | Clarify `HorizonScale/` and `jobdatabrain-tagger/` ownership | 15 min | Repo boundary clarity |
| 8 | Archive old `data/jobs/` docx off-repo | 30 min | Reduces clone size long-term |

---
*Last reviewed: 2026-04-27*
