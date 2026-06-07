<#
Creates the canonical DataCamp course scaffold for:

    Database Design

Canonical folder:

    D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design

Run:

    .\scaffold_database_design.ps1

Existing files are preserved by default. Use -Force only when you intentionally
want to replace scaffold files.

The four HTML shells are copied directly from the authoritative templates in
DataCamp\Course_starter. Their placeholders are intentionally retained until the
corresponding course artifact is populated from source material.
#>

[CmdletBinding()]
param(
    [string]$DataCampRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp',
    [string]$TemplateRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp\Course_starter',
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$courseName = 'Database Design'
$courseSlug = 'database_design'
$courseRoot = Join-Path $DataCampRoot "courses\$courseSlug"

$chapters = @(
    [pscustomobject]@{
        Number = 1
        Title  = 'Processing, Storing, and Organizing Data'
        Slug   = 'processing_storing_and_organizing_data'
    },
    [pscustomobject]@{
        Number = 2
        Title  = 'Database Schemas and Normalization'
        Slug   = 'database_schemas_and_normalization'
    },
    [pscustomobject]@{
        Number = 3
        Title  = 'Database Views'
        Slug   = 'database_views'
    },
    [pscustomobject]@{
        Number = 4
        Title  = 'Database Management'
        Slug   = 'database_management'
    }
)

function Ensure-Directory {
    param([Parameter(Mandatory)][string]$Path)

    if (Test-Path -LiteralPath $Path) {
        Write-Host "EXISTS   $Path" -ForegroundColor DarkCyan
        return
    }

    New-Item -ItemType Directory -Path $Path -Force | Out-Null
    Write-Host "FOLDER   $Path" -ForegroundColor Cyan
}

function Write-SafeTextFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        Write-Host "KEEP     $Path" -ForegroundColor DarkYellow
        return
    }

    $parent = Split-Path -Parent $Path
    Ensure-Directory -Path $parent
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Host "CREATED  $Path" -ForegroundColor Green
}

function Copy-SafeTemplate {
    param(
        [Parameter(Mandatory)][string]$TemplatePath,
        [Parameter(Mandatory)][string]$TargetPath
    )

    if (-not (Test-Path -LiteralPath $TemplatePath -PathType Leaf)) {
        throw "Required authoritative template was not found: $TemplatePath"
    }

    if ((Test-Path -LiteralPath $TargetPath) -and -not $Force) {
        Write-Host "KEEP     $TargetPath" -ForegroundColor DarkYellow
        return
    }

    $parent = Split-Path -Parent $TargetPath
    Ensure-Directory -Path $parent
    Copy-Item -LiteralPath $TemplatePath -Destination $TargetPath -Force
    Write-Host "COPIED   $TargetPath" -ForegroundColor Green
}

$paths = [ordered]@{
    Docs              = Join-Path $courseRoot 'docs'
    SourceMaterial    = Join-Path $courseRoot 'source_material'
    SourceArchive     = Join-Path $courseRoot 'source_material\archive'
    StudyPages        = Join-Path $courseRoot 'study_pages'
    Lab               = Join-Path $courseRoot 'lab'
    LabSql            = Join-Path $courseRoot 'lab\sql'
    ExpectedOutputs   = Join-Path $courseRoot 'lab\expected_outputs'
    LabNotes          = Join-Path $courseRoot 'lab\notes'
    LabSourceArchive  = Join-Path $courseRoot 'lab\source_archive'
}

Ensure-Directory -Path $courseRoot
foreach ($path in $paths.Values) {
    Ensure-Directory -Path $path
}

$courseIndexTemplate = Join-Path $TemplateRoot 'course_index_template.html'
$fieldGuideTemplate = Join-Path $TemplateRoot 'field_guide_template.html'
$sectionGuideTemplate = Join-Path $TemplateRoot 'section_field_guide_template.html'
$quickLookupTemplate = Join-Path $TemplateRoot 'sql_quick_lookup_template.html'

Copy-SafeTemplate -TemplatePath $courseIndexTemplate `
    -TargetPath (Join-Path $courseRoot 'index.html')

Copy-SafeTemplate -TemplatePath $fieldGuideTemplate `
    -TargetPath (Join-Path $paths.StudyPages 'field_guide.html')

Copy-SafeTemplate -TemplatePath $quickLookupTemplate `
    -TargetPath (Join-Path $paths.StudyPages 'sql_quick_lookup.html')

foreach ($chapter in $chapters) {
    $numberText = '{0:D2}' -f $chapter.Number
    $fileName = 'chapter_{0}_{1}_field_guide.html' -f $numberText, $chapter.Slug
    Copy-SafeTemplate -TemplatePath $sectionGuideTemplate `
        -TargetPath (Join-Path $paths.StudyPages $fileName)
}

$chapterMarkdown = ($chapters | ForEach-Object {
    "- Chapter $($_.Number): $($_.Title)"
}) -join [Environment]::NewLine

$readme = @"
# Database Design

Canonical course slug: `database_design`

Canonical course folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design
```

## Chapters

$chapterMarkdown

## Current status

- Platform: IN PROGRESS
- StudyBook package: PARTIAL
- Documentation: DEVELOPING
- Lab: DEVELOPING
- Recall: NEEDS REVIEW
- Interview readiness: NOT YET

HTML files begin as exact copies of the authoritative DataCamp templates and
are populated chapter by chapter from the supplied course material.
"@

Write-SafeTextFile -Path (Join-Path $courseRoot 'README.md') -Content $readme

$sessionState = @"
# StudyBubble Session State - Database Design

## Course identity

- Course: Database Design
- Slug: database_design
- Platform status: IN PROGRESS

## Chapter sequence

$chapterMarkdown

## Current working step

Process Chapter 1 source material and replace the Chapter 1 template
placeholders with source-supported content.
"@

Write-SafeTextFile `
    -Path (Join-Path $courseRoot 'STUDYBUBBLE_SESSION_STATE.md') `
    -Content $sessionState

$bom = @"
# Bill of Materials - Database Design

## Course identity

- Course title: Database Design
- Canonical slug: database_design
- Course folder: `courses/database_design`

## Source inventory available at startup

- Course curriculum screenshot: available in the supplied ZIP
- Course PDF: available in the supplied ZIP
- `potholeschicago.csv`: available in the supplied ZIP
- `reviews.csv`: available in the supplied ZIP
- Chapter videos/transcripts: not yet inventoried chapter by chapter

## Chapter list

$chapterMarkdown

## Planned artifacts

- `study_pages/field_guide.html`
- `study_pages/field_guide.md`
- Four chapter Field Guides
- `study_pages/sql_quick_lookup.html`
- `lab/lab_guide.html`
- `lab/lab_run_book.md`
- Course landing page and closeout documentation
"@

Write-SafeTextFile `
    -Path (Join-Path $paths.Docs 'BILL_OF_MATERIALS.md') `
    -Content $bom

$audit = @"
# Course Setup Audit - Database Design

## Scaffold checks

- [x] Stable number-free course slug used
- [x] Canonical course folder created
- [x] Four chapter filenames created from the curriculum
- [x] Course index copied from `course_index_template.html`
- [x] Main Field Guide copied from `field_guide_template.html`
- [x] Chapter guides copied from `section_field_guide_template.html`
- [x] SQL Quick Lookup copied from `sql_quick_lookup_template.html`
- [x] Existing files preserved unless `-Force` is supplied
- [ ] Course-specific placeholders populated
- [ ] Navigation validated after chapter population
- [ ] Lab scope validated
"@

Write-SafeTextFile `
    -Path (Join-Path $paths.Docs 'COURSE_SETUP_AUDIT.md') `
    -Content $audit

$sourceReadme = @"
# Source Material - Database Design

Place curriculum screenshots, transcripts, exercise notes, supplied datasets,
and other course evidence here. Preserve raw evidence under `archive/` after it
has been incorporated into the StudyBook artifacts.
"@

Write-SafeTextFile `
    -Path (Join-Path $paths.SourceMaterial 'README.md') `
    -Content $sourceReadme

Write-SafeTextFile `
    -Path (Join-Path $paths.SourceMaterial 'course_curriculum_outline.md') `
    -Content "# Database Design Curriculum Outline`n`n$chapterMarkdown`n"

Write-SafeTextFile `
    -Path (Join-Path $paths.SourceMaterial 'transcript_raw_combined.md') `
    -Content "# Database Design - Combined Raw Transcript`n`nSource transcripts will be appended here without rewriting the original evidence.`n"

Write-SafeTextFile `
    -Path (Join-Path $paths.SourceMaterial 'exercise_notes.md') `
    -Content "# Database Design - Exercise Notes`n`nCapture exercise prompts, answers, mistakes, and corrections here during the live course pass.`n"

$fieldGuideMarkdown = @"
# Database Design Field Guide

## Chapter Guides

$chapterMarkdown

## Course Big Picture

To be populated from the supplied course material.

## Core Concepts

To be populated chapter by chapter.

## Common Mistakes

To be populated from exercises and learner corrections.

## Interview Translation

To be populated with concise, interview-safe explanations.
"@

Write-SafeTextFile `
    -Path (Join-Path $paths.StudyPages 'field_guide.md') `
    -Content $fieldGuideMarkdown

$labReadme = @"
# Database Design Local Lab

This course includes supplied datasets that may support a practical database
modeling lab. The lab begins in DEVELOPING status and must not be described as
validated until runnable files and observed outputs exist.
"@

Write-SafeTextFile -Path (Join-Path $paths.Lab 'README.md') -Content $labReadme

Write-SafeTextFile `
    -Path (Join-Path $paths.Lab '00_how_to_run.md') `
    -Content "# How to Run the Database Design Lab`n`nThe runnable workflow will be added after the supplied datasets and course exercises are inspected.`n"

Write-SafeTextFile `
    -Path (Join-Path $paths.Lab 'lab_run_book.md') `
    -Content "# Database Design Lab Run Book`n`n## Status`n`nDEVELOPING - no validated execution evidence has been recorded yet.`n"

Write-SafeTextFile `
    -Path (Join-Path $paths.Lab 'lab_guide.html') `
    -Content '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Database Design Lab Guide</title></head><body><main><h1>Database Design Lab Guide</h1><p>Status: Developing. This page will be populated after the course lab scope is validated.</p><p><a href="../index.html">Course Home</a></p></main></body></html>'

Write-SafeTextFile `
    -Path (Join-Path $paths.ExpectedOutputs 'README.md') `
    -Content "# Expected Outputs`n`nRecord only outputs that have actually been observed and validated.`n"

Write-SafeTextFile `
    -Path (Join-Path $paths.LabNotes 'troubleshooting.md') `
    -Content "# Database Design Lab Troubleshooting`n`nCapture real setup and execution problems here as they occur.`n"

Write-Host ''
Write-Host 'Database Design scaffold is ready.' -ForegroundColor Green
Write-Host "Course root: $courseRoot" -ForegroundColor White
Write-Host ''
Write-Host 'Chapter files:' -ForegroundColor Cyan
foreach ($chapter in $chapters) {
    $numberText = '{0:D2}' -f $chapter.Number
    Write-Host ('  chapter_{0}_{1}_field_guide.html' -f $numberText, $chapter.Slug)
}
