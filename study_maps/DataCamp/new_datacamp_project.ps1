<#
Creates a canonical DataCamp project folder with safe under-construction stubs.

Example for this project:

.\new_datacamp_project.ps1 `
  -ProjectName "Analyzing Students' Mental Health" `
  -ProjectSlug "analyzing_students_mental_health" `
  -SkillTrackName "SQL Fundamentals" `
  -SkillTrackFolder "01_sql_fundamentals"

By default, existing files are preserved. Use -Force only when you intentionally
want to replace generated stub files.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectName,

    [Parameter(Mandatory)]
    [ValidatePattern('^[a-z0-9]+(?:_[a-z0-9]+)*$')]
    [string]$ProjectSlug,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$SkillTrackName,

    [Parameter(Mandatory)]
    [ValidatePattern('^[a-z0-9]+(?:_[a-z0-9]+)*$')]
    [string]$SkillTrackFolder,

    [string]$DataCampRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp',

    [ValidatePattern('^[a-z0-9_]+\.html$')]
    [string]$QuickLookupName = 'sql_quick_lookup.html',

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-SafeFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        Write-Host "KEEP     $Path" -ForegroundColor DarkYellow
        return
    }

    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Host "CREATED  $Path" -ForegroundColor Green
}

function New-HtmlStub {
    param(
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Heading,
        [Parameter(Mandatory)][string]$Message,
        [string]$BackHref = '../index.html',
        [string]$BackLabel = 'Back to Project Home'
    )

@"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$Title</title>
  <style>
    :root {
      --bg: #0d1117;
      --panel: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #9da7b3;
      --green: #03ef62;
      --blue: #58a6ff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }
    header { height: 4px; background: linear-gradient(90deg, var(--green), var(--blue)); }
    main {
      width: min(920px, calc(100% - 32px));
      margin: 0 auto;
      padding: 34px 0 48px;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
    }
    h1 { margin-top: 0; }
    p { color: var(--muted); }
    a { color: var(--green); text-decoration: none; font-weight: 700; }
    code { color: var(--blue); }
  </style>
</head>
<body>
  <header></header>
  <main>
    <section>
      <h1>$Heading</h1>
      <p><strong>Status:</strong> Under construction</p>
      <p>$Message</p>
      <p><a href="$BackHref">$BackLabel</a></p>
    </section>
  </main>
</body>
</html>
"@
}

$projectRoot = Join-Path $DataCampRoot "projects\$ProjectSlug"
$docsRoot = Join-Path $projectRoot 'docs'
$sourceRoot = Join-Path $projectRoot 'source_material'
$studyRoot = Join-Path $projectRoot 'study_pages'
$labRoot = Join-Path $projectRoot 'lab'
$sqlRoot = Join-Path $labRoot 'sql'
$expectedRoot = Join-Path $labRoot 'expected_outputs'
$notesRoot = Join-Path $labRoot 'notes'

$folders = @(
    $projectRoot,
    $docsRoot,
    $sourceRoot,
    $studyRoot,
    $labRoot,
    $sqlRoot,
    $expectedRoot,
    $notesRoot
)

foreach ($folder in $folders) {
    if (-not (Test-Path -LiteralPath $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "FOLDER   $folder" -ForegroundColor Cyan
    }
    else {
        Write-Host "EXISTS   $folder" -ForegroundColor DarkCyan
    }
}

$fieldGuide = New-HtmlStub `
    -Title "$ProjectName | Project Field Guide" `
    -Heading "$ProjectName Project Field Guide" `
    -Message 'This page will explain the dataset, analysis question, SQL reasoning, final query, findings, mistakes, and reusable lessons.'

Write-SafeFile `
    -Path (Join-Path $studyRoot 'project_field_guide.html') `
    -Content $fieldGuide

$quickLookup = New-HtmlStub `
    -Title "$ProjectName | SQL Quick Lookup" `
    -Heading "$ProjectName SQL Quick Lookup" `
    -Message 'This compact page will hold the SQL clauses, aggregation patterns, filtering rules, aliases, rounding, and common traps used by the project.'

Write-SafeFile `
    -Path (Join-Path $studyRoot $QuickLookupName) `
    -Content $quickLookup

$labGuide = New-HtmlStub `
    -Title "$ProjectName | Lab Guide" `
    -Heading "$ProjectName Lab Guide" `
    -Message 'This page will document the local PostgreSQL setup, students table, CSV load process, practiced queries, expected outputs, and troubleshooting notes.'

Write-SafeFile `
    -Path (Join-Path $labRoot 'lab_guide.html') `
    -Content $labGuide

$indexHtml = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$ProjectName | DataCamp StudyBook</title>
  <style>
    :root {
      --bg: #0d1117;
      --panel: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #9da7b3;
      --green: #03ef62;
      --blue: #58a6ff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }
    header { height: 4px; background: linear-gradient(90deg, var(--green), var(--blue)); }
    main {
      width: min(1000px, calc(100% - 32px));
      margin: 0 auto;
      padding: 34px 0 48px;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 18px;
    }
    h1, h2 { margin-top: 0; }
    p, li { color: var(--muted); }
    a { color: var(--green); text-decoration: none; font-weight: 700; }
    code { color: var(--blue); }
  </style>
</head>
<body>
  <header></header>
  <main>
    <section>
      <h1>$ProjectName</h1>
      <p><strong>Type:</strong> DataCamp SQL Project</p>
      <p><strong>Status:</strong> Under construction</p>
      <p><strong>Skill track:</strong> $SkillTrackName</p>
      <p><strong>Canonical slug:</strong> <code>$ProjectSlug</code></p>
    </section>

    <section>
      <h2>Project Materials</h2>
      <ul>
        <li><a href="study_pages/project_field_guide.html">Project Field Guide</a></li>
        <li><a href="study_pages/$QuickLookupName">SQL Quick Lookup</a></li>
        <li><a href="lab/lab_guide.html">Local Lab Guide</a></li>
        <li><a href="docs/PROJECT_SETUP_AUDIT.md">Project Setup Audit</a></li>
        <li><a href="README.md">README</a></li>
      </ul>
    </section>

    <section>
      <h2>Navigation</h2>
      <p><a href="../../skill_tracks/$SkillTrackFolder/index.html">Back to $SkillTrackName</a></p>
      <p><a href="../index.html">Back to DataCamp Projects</a></p>
      <p><a href="../../index.html">Back to DataCamp StudyBook</a></p>
    </section>
  </main>
</body>
</html>
"@

Write-SafeFile `
    -Path (Join-Path $projectRoot 'index.html') `
    -Content $indexHtml

$readme = @"
# $ProjectName

Canonical StudyBook package for the DataCamp project.

## Identity

- Project: $ProjectName
- Canonical slug: ``$ProjectSlug``
- Type: DataCamp SQL Project
- Skill track: $SkillTrackName
- Status: Under construction

## Primary opening page

``````text
index.html
``````

## Package structure

``````text
$ProjectSlug/
|-- index.html
|-- README.md
|-- docs/
|   |-- PROJECT_SETUP_AUDIT.md
|-- source_material/
|   |-- README.md
|-- study_pages/
|   |-- project_field_guide.html
|   |-- $QuickLookupName
|-- lab/
    |-- lab_guide.html
    |-- sql/
    |   |-- 00_create_students_table.sql
    |   |-- 01_project_solution.sql
    |   |-- 02_practice_queries.sql
    |-- expected_outputs/
    |   |-- README.md
    |-- notes/
        |-- troubleshooting.md
``````

## Working rule

The project folder contains the study package and the local evidence from the completed PostgreSQL practice. The skill-track page owns project ordering and navigation.

## Next step

Replace the stubs one file at a time using the real dataset, SQL, outputs, and lessons learned.
"@

Write-SafeFile `
    -Path (Join-Path $projectRoot 'README.md') `
    -Content $readme

$setupAudit = @"
# Project Setup Audit

## Project identity

- Project: $ProjectName
- Canonical slug: ``$ProjectSlug``
- Skill track: $SkillTrackName
- Status: Scaffold created; content pending

## Expected source evidence

- DataCamp project instructions or screenshots
- Students CSV dataset or source reference
- Local PostgreSQL table definition
- CSV load script or load notes
- Final accepted SQL query
- Practiced queries and observed outputs
- Mistakes, corrections, and lessons learned

## Planned study artifacts

- Project landing page
- Project Field Guide
- SQL Quick Lookup
- Local Lab Guide
- SQL source files
- Expected-output notes
- Troubleshooting notes
- README
- Skill-track backlink
- Projects-library backlink

## Validation checklist

- [ ] Project landing page opens
- [ ] All local links resolve
- [ ] Final SQL is preserved
- [ ] Dataset columns are documented
- [ ] Local load process is documented
- [ ] Expected result is preserved
- [ ] Skill-track page links to this project
- [ ] Projects landing page links to this project
"@

Write-SafeFile `
    -Path (Join-Path $docsRoot 'PROJECT_SETUP_AUDIT.md') `
    -Content $setupAudit

$sourceReadme = @"
# Source Material

Place project evidence here:

- DataCamp instructions and screenshots
- dataset notes or archived source files
- raw project prompt
- accepted answer
- exercise notes
- local setup notes

Raw sources are evidence. Distilled learning material belongs under ``study_pages``. Runnable SQL belongs under ``lab\sql``.
"@

Write-SafeFile `
    -Path (Join-Path $sourceRoot 'README.md') `
    -Content $sourceReadme

$createTableSql = @"
-- $ProjectName
-- Local students table setup.
-- Replace this stub with the verified table definition used by the project.

-- Status: UNDER CONSTRUCTION
"@

Write-SafeFile `
    -Path (Join-Path $sqlRoot '00_create_students_table.sql') `
    -Content $createTableSql

$solutionSql = @"
-- $ProjectName
-- Preserve the final accepted DataCamp project query here.

-- Status: UNDER CONSTRUCTION
"@

Write-SafeFile `
    -Path (Join-Path $sqlRoot '01_project_solution.sql') `
    -Content $solutionSql

$practiceSql = @"
-- $ProjectName
-- Add supporting exploration and muscle-memory queries here.

-- Status: UNDER CONSTRUCTION
"@

Write-SafeFile `
    -Path (Join-Path $sqlRoot '02_practice_queries.sql') `
    -Content $practiceSql

$expectedReadme = @"
# Expected Outputs

Record verified outputs from the local PostgreSQL project practice here.

Include:

- query name
- expected columns
- expected row count when stable
- representative output
- comparison with the accepted DataCamp result
"@

Write-SafeFile `
    -Path (Join-Path $expectedRoot 'README.md') `
    -Content $expectedReadme

$troubleshooting = @"
# Troubleshooting

Record project-specific setup and query problems here.

Suggested sections:

- PostgreSQL connection
- database and schema selection
- CSV loading
- column types
- NULL handling
- grouping and filtering mistakes
- result differences between local PostgreSQL and DataCamp
"@

Write-SafeFile `
    -Path (Join-Path $notesRoot 'troubleshooting.md') `
    -Content $troubleshooting

Write-Host ''
Write-Host 'DataCamp project scaffold complete.' -ForegroundColor Green
Write-Host "Project root: $projectRoot"
Write-Host "Open:         $(Join-Path $projectRoot 'index.html')"
Write-Host 'Existing files were preserved unless -Force was supplied.' -ForegroundColor DarkYellow
Write-Host 'No Git operations were performed.' -ForegroundColor DarkYellow
