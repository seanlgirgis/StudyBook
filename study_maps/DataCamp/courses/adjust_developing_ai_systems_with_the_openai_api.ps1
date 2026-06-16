[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$CourseRoot = "D:\Workarea\StudyBook\study_maps\DataCamp\courses\developing_ai_systems_with_the_openai_api"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Backup-File {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string]$BackupRoot,
        [Parameter(Mandatory)] [string]$Root
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return }

    $relative = $Path.Substring($Root.Length).TrimStart('\')
    $destination = Join-Path $BackupRoot $relative
    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
    Copy-Item -LiteralPath $Path -Destination $destination -Force
}

function Replace-TextInFile {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [hashtable]$Replacements
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return }

    $content = [System.IO.File]::ReadAllText($Path)
    $original = $content

    foreach ($key in $Replacements.Keys) {
        $content = $content.Replace([string]$key, [string]$Replacements[$key])
    }

    if ($content -ne $original) {
        Write-Utf8NoBom -Path $Path -Content $content
        Write-Host "Updated text references: $Path"
    }
}

if (-not (Test-Path -LiteralPath $CourseRoot -PathType Container)) {
    throw "Course folder not found: $CourseRoot"
}

$requiredFiles = @(
    "index.html",
    "README.md",
    "study_pages\field_guide.html",
    "study_pages\chapter_01_structuring_end_to_end_applications_field_guide.html",
    "study_pages\chapter_02_function_calling_field_guide.html",
    "study_pages\chapter_03_best_practices_for_production_applications_field_guide.html"
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $CourseRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Required course file is missing: $fullPath"
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupRoot = Join-Path $CourseRoot "source_material\archive\setup_adjustment_backup_$timestamp"
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

$filesToBackup = @(
    "README.md",
    "STUDYBUBBLE_SESSION_STATE.md",
    "index.html",
    "docs\BILL_OF_MATERIALS.md",
    "docs\COURSE_SETUP_AUDIT.md",
    "source_material\course_curriculum_outline.md",
    "study_pages\field_guide.html",
    "study_pages\field_guide.md",
    "study_pages\sql_quick_lookup.html",
    "study_pages\openai_api_quick_lookup.html",
    "lab\README.md",
    "lab\00_how_to_run.md",
    "lab\lab_run_book.md"
)

foreach ($relativePath in $filesToBackup) {
    Backup-File -Path (Join-Path $CourseRoot $relativePath) -BackupRoot $backupRoot -Root $CourseRoot
}

Write-Host "Backup created: $backupRoot"

# -----------------------------------------------------------------------------
# 1. Correct the domain-specific quick lookup filename.
# -----------------------------------------------------------------------------
$oldQuickLookup = Join-Path $CourseRoot "study_pages\sql_quick_lookup.html"
$newQuickLookup = Join-Path $CourseRoot "study_pages\openai_api_quick_lookup.html"

if (Test-Path -LiteralPath $oldQuickLookup -PathType Leaf) {
    if (Test-Path -LiteralPath $newQuickLookup -PathType Leaf) {
        Write-Warning "Both quick-lookup files exist. The existing OpenAI API file was preserved; the SQL-named file was not removed."
    }
    elseif ($PSCmdlet.ShouldProcess($oldQuickLookup, "Rename to openai_api_quick_lookup.html")) {
        Move-Item -LiteralPath $oldQuickLookup -Destination $newQuickLookup
        Write-Host "Renamed quick lookup: openai_api_quick_lookup.html"
    }
}

# Replace references while preserving the authoritative HTML layouts.
$referenceReplacements = [ordered]@{
    "sql_quick_lookup.html"   = "openai_api_quick_lookup.html"
    "SQL Join Quick Lookup"   = "OpenAI API Quick Lookup"
    "Open SQL Quick Lookup"   = "Open OpenAI API Quick Lookup"
    "SQL Quick Lookup"        = "OpenAI API Quick Lookup"
}

Get-ChildItem -LiteralPath $CourseRoot -Recurse -File |
    Where-Object { $_.Extension -in ".html", ".md" } |
    ForEach-Object { Replace-TextInFile -Path $_.FullName -Replacements $referenceReplacements }

# -----------------------------------------------------------------------------
# 2. Remove the unused Chapter 4 template remnants from whole-course pages.
# -----------------------------------------------------------------------------
$indexPath = Join-Path $CourseRoot "index.html"
$indexContent = [System.IO.File]::ReadAllText($indexPath)
$indexOriginal = $indexContent
$indexContent = [regex]::Replace(
    $indexContent,
    '(?ms)^\s*<li><a href="\{\{CHAPTER_04_FILE\}\}">\{\{CHAPTER_04_TITLE\}\}</a></li>\s*',
    ''
)
$indexContent = [regex]::Replace(
    $indexContent,
    '(?ms)\s*<article class="chapter-card">\s*<a href="\{\{CHAPTER_04_FILE\}\}">\s*<h3>\{\{CHAPTER_04_TITLE\}\}</h3>\s*<p>\{\{CHAPTER_04_SUMMARY\}\}</p>\s*</a>\s*</article>',
    ''
)
if ($indexContent -ne $indexOriginal) {
    Write-Utf8NoBom -Path $indexPath -Content $indexContent
    Write-Host "Removed Chapter 4 remnants from index.html"
}

$fieldGuidePath = Join-Path $CourseRoot "study_pages\field_guide.html"
$fieldGuideContent = [System.IO.File]::ReadAllText($fieldGuidePath)
$fieldGuideOriginal = $fieldGuideContent
$fieldGuideContent = [regex]::Replace(
    $fieldGuideContent,
    '(?ms)\s*<article class="chapter-card">\s*<h3><a href="\{\{CHAPTER_04_FILE\}\}">\{\{CHAPTER_04_TITLE\}\}</a></h3>\s*<p>\{\{CHAPTER_04_SUMMARY\}\}</p>\s*</article>',
    ''
)
if ($fieldGuideContent -ne $fieldGuideOriginal) {
    Write-Utf8NoBom -Path $fieldGuidePath -Content $fieldGuideContent
    Write-Host "Removed Chapter 4 remnants from field_guide.html"
}

# -----------------------------------------------------------------------------
# 3. Replace SQL-oriented lab structure with a Python-oriented structure.
# -----------------------------------------------------------------------------
$pythonRoot = Join-Path $CourseRoot "lab\python"
$pythonChapterFolders = @(
    "chapter_01_structuring_end_to_end_applications",
    "chapter_02_function_calling",
    "chapter_03_best_practices_for_production_applications"
)

New-Item -ItemType Directory -Path $pythonRoot -Force | Out-Null
foreach ($folder in $pythonChapterFolders) {
    New-Item -ItemType Directory -Path (Join-Path $pythonRoot $folder) -Force | Out-Null
}

$sqlFolder = Join-Path $CourseRoot "lab\sql"
if (Test-Path -LiteralPath $sqlFolder -PathType Container) {
    $sqlItems = @(Get-ChildItem -LiteralPath $sqlFolder -Force)
    if ($sqlItems.Count -eq 0) {
        Remove-Item -LiteralPath $sqlFolder -Force
        Write-Host "Removed empty lab\sql folder"
    }
    else {
        Write-Warning "lab\sql contains files and was preserved. Review it manually before moving anything."
    }
}

Write-Utf8NoBom -Path (Join-Path $pythonRoot "README.md") -Content @'
# Python Lab Workspace

Runnable OpenAI API exercises belong here, grouped by course chapter.

- `chapter_01_structuring_end_to_end_applications`
- `chapter_02_function_calling`
- `chapter_03_best_practices_for_production_applications`

Do not add invented completion evidence. Record a script as validated only after it runs successfully.
'@

# -----------------------------------------------------------------------------
# 4. Populate course metadata and source inventory from the supplied curriculum.
# -----------------------------------------------------------------------------
Write-Utf8NoBom -Path (Join-Path $CourseRoot "README.md") -Content @'
# Developing AI Systems with the OpenAI API

Canonical DataCamp course package for the **Developing AI Applications** skill track.

- Track position: 6
- Canonical slug: `developing_ai_systems_with_the_openai_api`
- Level: Intermediate
- Estimated duration: 3 hours
- Curriculum: 3 chapters, 11 videos, 36 exercises
- Course update shown by DataCamp: April 2026
- Platform status: NOT STARTED
- StudyBook package: SCAFFOLDED

## Canonical path

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\developing_ai_systems_with_the_openai_api
```

## Course chapters

1. Structuring End-to-End Applications
2. Function Calling
3. Best Practices for Production Applications

## Main resources

- `study_pages/field_guide.html`
- `study_pages/openai_api_quick_lookup.html`
- `study_pages/chapter_01_structuring_end_to_end_applications_field_guide.html`
- `study_pages/chapter_02_function_calling_field_guide.html`
- `study_pages/chapter_03_best_practices_for_production_applications_field_guide.html`
- `lab/lab_run_book.md`

Chapter guides remain template shells until their source material is studied and supplied.
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "source_material\course_curriculum_outline.md") -Content @'
# Developing AI Systems with the OpenAI API — Curriculum Outline

## Course metadata

- Level: Intermediate
- Updated: April 2026
- Estimated duration: 3 hours
- Videos: 11
- Exercises: 36
- Chapters: 3

## Chapter 1 — Structuring End-to-End Applications

1. Structuring an API call
2. Decoding the response
3. Formatting model response as JSON
4. Handling errors
5. Interpreting error messages
6. Handling exceptions
7. Batching
8. Avoiding rate limits with retry
9. Batching messages
10. Setting token limits

## Chapter 2 — Function Calling

1. Defining function calling
2. Function calling definition
3. Function calling steps
4. Extracting structured data from text
5. Using the tools parameter
6. Building a function dictionary
7. Extracting the response
8. Working with multiple functions
9. Parallel function calling
10. Setting a specific function
11. Avoiding inconsistent responses
12. Calling external APIs
13. Defining a function with external APIs
14. Calling an external API
15. Handling the response with external API calls

## Chapter 3 — Best Practices for Production Applications

1. Moderation
2. Mitigating prompt injection
3. Moderation API
4. Adding guardrails
5. Validation
6. Potential for model errors
7. Adversarial testing
8. Safety best practices
9. Minimizing model risks
10. Including end-user IDs
11. Wrap-up

## Source status

- Course overview screenshot: supplied in the course chat
- Chapter videos/transcripts: not yet supplied
- Exercise notes and solutions: not yet supplied
- Runnable local evidence: not yet recorded
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "docs\BILL_OF_MATERIALS.md") -Content @'
# Bill of Materials — Developing AI Systems with the OpenAI API

## Identity

- Canonical slug: `developing_ai_systems_with_the_openai_api`
- Track: Developing AI Applications
- Track position: 6
- Level: Intermediate
- DataCamp update shown: April 2026
- Estimated duration: 3 hours
- Curriculum size: 3 chapters, 11 videos, 36 exercises

## Source inventory

| Source | Status | Notes |
|---|---|---|
| Course overview screenshot | AVAILABLE | Supplies title, metadata, chapters, and lesson names |
| Chapter videos | MISSING | Supply chapter by chapter |
| Transcripts | MISSING | `source_material/transcript_raw_combined.md` is still a shell |
| Exercise notes | MISSING | Capture during the live course pass |
| Local Python code | NOT STARTED | Store under `lab/python/` |
| Expected outputs | NOT STARTED | Record only after execution |

## Planned study artifacts

- `study_pages/field_guide.html`
- `study_pages/field_guide.md`
- `study_pages/openai_api_quick_lookup.html`
- Three chapter field guides
- `lab/lab_run_book.md`
- Python chapter workspaces under `lab/python/`

## Core topic inventory

### Chapter 1

API request structure, response decoding, JSON output, errors, exceptions, batching, retry behavior, rate limits, and token limits.

### Chapter 2

Tool definitions, the `tools` parameter, tool-call extraction, function dictionaries, multiple and parallel functions, forced tool selection, external API execution, and returning tool results.

### Chapter 3

Moderation, prompt-injection mitigation, guardrails, validation, model-error handling, adversarial testing, safety practices, risk reduction, and end-user identifiers.

## Fast-review priorities

- Request-to-response lifecycle
- Structured outputs and validation
- Retry versus batching
- Tool-calling lifecycle
- Separation between model selection and application execution
- Moderation and prompt-injection defenses

## Open items

- Populate chapter pages only from supplied chapter sources and completed exercises.
- Validate examples against the OpenAI API version taught by the course.
- Record actual local run evidence before marking the lab complete.
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "docs\COURSE_SETUP_AUDIT.md") -Content @'
# Developing AI Systems with the OpenAI API — Course Setup Audit

## Setup findings

| Check | Result |
|---|---|
| Canonical folder | PASS |
| Stable number-free slug | PASS |
| Chapter count | PASS — 3 chapters |
| Chapter filenames | PASS |
| Track position | CORRECTED — 6 |
| Chapter 4 template remnants | REMOVED from whole-course pages |
| Quick lookup domain | CORRECTED to OpenAI API |
| Python lab workspace | CREATED |
| Empty SQL lab folder | REMOVED when safe |
| Curriculum outline | POPULATED from supplied screenshot |
| Bill of Materials | POPULATED |
| Chapter content | PENDING source intake |
| HTML placeholders | EXPECTED in scaffold shells; resolve during chapter/course builds |
| Navigation validation | PENDING chapter population |

## Honest status

- Platform: NOT STARTED
- StudyBook package: PARTIAL
- Documentation: DEVELOPING
- Lab: DEVELOPING
- Recall: NEEDS REVIEW
- Interview readiness: NOT YET

## Next action

Process Chapter 1 source material and replace the Chapter 1 template placeholders without changing the authoritative template layout.
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "lab\README.md") -Content @'
# Course Lab

This course uses Python exercises for OpenAI API application patterns.

Runnable files belong under:

```text
lab/python/
```

Expected outputs belong under `lab/expected_outputs/`, and troubleshooting notes belong under `lab/notes/`.

Do not record a script as validated until it has been executed successfully.
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "lab\00_how_to_run.md") -Content @'
# How to Run the Python Lab

From the canonical course folder:

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\developing_ai_systems_with_the_openai_api\lab\python
```

Use the Python environment already configured for the earlier OpenAI API courses. Keep API keys in environment variables; never place a real key in source files.

Chapter-specific commands will be added when runnable scripts are created.
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "lab\lab_run_book.md") -Content @'
# Lab Run Book — Developing AI Systems with the OpenAI API

## Purpose

Practice production-oriented OpenAI API application patterns without inventing completion evidence.

## Chapter workspaces

1. `python/chapter_01_structuring_end_to_end_applications`
2. `python/chapter_02_function_calling`
3. `python/chapter_03_best_practices_for_production_applications`

## Planned Chapter 1 practice

- Decode a model response safely
- Request structured JSON
- Catch and inspect API exceptions
- Add bounded retry behavior
- Batch several inputs
- Control output-token limits

## Planned Chapter 2 practice

- Define one tool schema
- Read a tool call
- Execute a local Python function
- Return a tool result to the model
- Support multiple tools
- Call an external API through application code

## Planned Chapter 3 practice

- Moderate input and output
- Add basic prompt-injection defenses
- Validate model output
- Create adversarial test cases
- Attach a stable end-user identifier where supported

## Evidence policy

For every completed exercise, record:

- script path
- command used
- observed output
- mistake or correction
- validation date
'@

Write-Utf8NoBom -Path (Join-Path $CourseRoot "STUDYBUBBLE_SESSION_STATE.md") -Content @'
# Session State — Developing AI Systems with the OpenAI API

## Current position

- Track: Developing AI Applications
- Track position: 6
- Course scaffold: corrected and ready
- Active chapter: Chapter 1 — Structuring End-to-End Applications
- Platform progress: 0%

## Completed setup work

- Confirmed three-chapter curriculum
- Corrected track position
- Renamed the quick lookup for the OpenAI API domain
- Created Python chapter lab folders
- Removed unused Chapter 4 template remnants
- Populated curriculum outline, BOM, and setup audit

## Next step

Supply and process Chapter 1 source material, then build the Chapter 1 field guide and runnable Python exercises incrementally.
'@

# -----------------------------------------------------------------------------
# 5. Validation report.
# -----------------------------------------------------------------------------
$placeholderReport = Get-ChildItem -LiteralPath $CourseRoot -Recurse -Filter *.html -File |
    ForEach-Object {
        $text = [System.IO.File]::ReadAllText($_.FullName)
        [pscustomobject]@{
            File = $_.FullName.Substring($CourseRoot.Length).TrimStart('\')
            Placeholders = ([regex]::Matches($text, '\{\{[^}]+\}\}')).Count
            Chapter4Refs = ([regex]::Matches($text, 'CHAPTER_04')).Count
        }
    }

Write-Host ""
Write-Host "Adjustment complete." -ForegroundColor Green
Write-Host "Course root: $CourseRoot"
Write-Host "Backup:      $backupRoot"
Write-Host ""
$placeholderReport | Format-Table -AutoSize

$chapter4Total = ($placeholderReport | Measure-Object -Property Chapter4Refs -Sum).Sum
if ($chapter4Total -gt 0) {
    Write-Warning "Chapter 4 references remain in one or more HTML files. Review the table above."
}
else {
    Write-Host "Validation: no Chapter 4 placeholder references remain." -ForegroundColor Green
}

if (-not (Test-Path -LiteralPath $newQuickLookup -PathType Leaf)) {
    Write-Warning "OpenAI API quick lookup file was not found after adjustment."
}
else {
    Write-Host "Validation: OpenAI API quick lookup exists." -ForegroundColor Green
}

Write-Host ""
Write-Host "Note: chapter and whole-course HTML files intentionally remain content shells until source material is processed."
