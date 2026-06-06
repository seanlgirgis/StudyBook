<#
Creates a canonical DataCamp course folder with safe under-construction stubs.

Example:

.\new_datacamp_course.ps1 `
  -CourseName "Intermediate SQL" `
  -CourseSlug "intermediate_sql" `
  -TrackName "SQL Fundamentals" `
  -TrackPosition 2 `
  -Chapters @(
    "Selecting Data",
    "Filtering Records",
    "Aggregate Functions",
    "Sorting and Grouping"
  )
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$CourseName,

    [Parameter(Mandatory)]
    [ValidatePattern('^[a-z0-9]+(?:_[a-z0-9]+)*$')]
    [string]$CourseSlug,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$TrackName,

    [Parameter(Mandatory)]
    [ValidateRange(1, 999)]
    [int]$TrackPosition,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string[]]$Chapters,

    [string]$DataCampRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp',

    [ValidatePattern('^[a-z0-9_]+\.html$')]
    [string]$QuickLookupName = 'sql_quick_lookup.html',

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-Slug {
    param([Parameter(Mandatory)][string]$Text)

    $slug = $Text.ToLowerInvariant()
    $slug = $slug -replace '[^a-z0-9]+', '_'
    $slug = $slug.Trim('_')

    if ([string]::IsNullOrWhiteSpace($slug)) {
        throw "Could not create a slug from: $Text"
    }

    $slug
}

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
        [string]$BackHref = '../index.html'
    )

@"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$Title</title>
  <style>
    body {
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: #0d1117;
      color: #e6edf3;
      line-height: 1.6;
    }
    main {
      width: min(900px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 48px;
    }
    section {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 14px;
      padding: 22px;
    }
    h1 { margin-top: 0; }
    p { color: #9da7b3; }
    a {
      color: #03ef62;
      text-decoration: none;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <main>
    <section>
      <h1>$Heading</h1>
      <p><strong>Status:</strong> Under construction</p>
      <p>$Message</p>
      <p><a href="$BackHref">Back to Course Home</a></p>
    </section>
  </main>
</body>
</html>
"@
}

$courseRoot = Join-Path $DataCampRoot "courses\$CourseSlug"
$docsRoot = Join-Path $courseRoot 'docs'
$labRoot = Join-Path $courseRoot 'lab'
$sourceRoot = Join-Path $courseRoot 'source_material'
$studyRoot = Join-Path $courseRoot 'study_pages'

foreach ($folder in @($courseRoot, $docsRoot, $labRoot, $sourceRoot, $studyRoot)) {
    if (-not (Test-Path -LiteralPath $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "FOLDER   $folder" -ForegroundColor Cyan
    }
    else {
        Write-Host "EXISTS   $folder" -ForegroundColor DarkCyan
    }
}

$chapterLinks = @()
$chapterSummary = @()
$chapterTree = @()

for ($i = 0; $i -lt $Chapters.Count; $i++) {
    $chapterNumber = $i + 1
    $numberText = '{0:D2}' -f $chapterNumber
    $chapterName = $Chapters[$i].Trim()
    $chapterSlug = ConvertTo-Slug $chapterName
    $chapterFile = "chapter_${numberText}_${chapterSlug}_field_guide.html"

    $chapterHtml = New-HtmlStub `
        -Title "$CourseName | Chapter $chapterNumber - $chapterName" `
        -Heading "Chapter $chapterNumber - $chapterName" `
        -Message "This chapter Field Guide will be populated from the course curriculum, videos, transcripts, exercises, and learner notes."

    Write-SafeFile `
        -Path (Join-Path $studyRoot $chapterFile) `
        -Content $chapterHtml

    $chapterLinks += "        <li><a href=`"study_pages/$chapterFile`">Chapter $chapterNumber - $chapterName</a></li>"
    $chapterSummary += "- Chapter ${chapterNumber}: $chapterName"
    $chapterTree += "    |-- $chapterFile"
}

$fieldGuide = New-HtmlStub `
    -Title "$CourseName | Field Guide" `
    -Heading "$CourseName Field Guide" `
    -Message "This accumulated Field Guide will become the whole-course memory map and cross-chapter review page."

Write-SafeFile `
    -Path (Join-Path $studyRoot 'field_guide.html') `
    -Content $fieldGuide

$quickLookup = New-HtmlStub `
    -Title "$CourseName | Quick Lookup" `
    -Heading "$CourseName Quick Lookup" `
    -Message "This searchable page will contain the smallest useful syntax patterns, rules, and common traps."

Write-SafeFile `
    -Path (Join-Path $studyRoot $QuickLookupName) `
    -Content $quickLookup

$labGuide = New-HtmlStub `
    -Title "$CourseName | Lab Guide" `
    -Heading "$CourseName Lab Guide" `
    -Message "The lab strategy is not decided yet. This may become a full course-local lab or remain a lightweight note if DataCamp exercises are sufficient."

Write-SafeFile `
    -Path (Join-Path $labRoot 'lab_guide.html') `
    -Content $labGuide

$indexHtml = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$CourseName | DataCamp StudyBook</title>
  <style>
    body {
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: #0d1117;
      color: #e6edf3;
      line-height: 1.6;
    }
    main {
      width: min(980px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 48px;
    }
    section {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 18px;
    }
    h1, h2 { margin-top: 0; }
    p, li { color: #9da7b3; }
    a {
      color: #03ef62;
      text-decoration: none;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <main>
    <section>
      <h1>$CourseName</h1>
      <p><strong>Status:</strong> Under construction</p>
      <p><strong>Track:</strong> $TrackName - Course $TrackPosition</p>
      <p><strong>Canonical slug:</strong> <code>$CourseSlug</code></p>
    </section>

    <section>
      <h2>Course Materials</h2>
      <ul>
        <li><a href="study_pages/field_guide.html">Accumulated Field Guide</a></li>
        <li><a href="study_pages/$QuickLookupName">Quick Lookup</a></li>
$($chapterLinks -join "`r`n")
        <li><a href="lab/lab_guide.html">Lab Guide</a></li>
        <li><a href="docs/BILL_OF_MATERIALS.md">Bill of Materials</a></li>
        <li><a href="README.md">README</a></li>
      </ul>
    </section>

    <section>
      <p><a href="../index.html">Back to Course Library</a></p>
      <p><a href="../../index.html">Back to DataCamp StudyBook</a></p>
    </section>
  </main>
</body>
</html>
"@

Write-SafeFile `
    -Path (Join-Path $courseRoot 'index.html') `
    -Content $indexHtml

$readme = @"
# $CourseName

Canonical DataCamp course package.

## Identity

- Course: $CourseName
- Canonical slug: ``$CourseSlug``
- Track: $TrackName
- Track position: Course $TrackPosition
- Status: Under construction

## Chapters

$($chapterSummary -join "`r`n")

## Primary opening page

``````text
index.html
``````

## Package structure

``````text
$CourseSlug/
|-- index.html
|-- README.md
|-- docs/
|   |-- BILL_OF_MATERIALS.md
|-- lab/
|   |-- lab_guide.html
|-- source_material/
|   |-- README.md
|-- study_pages/
|   |-- field_guide.html
|   |-- $QuickLookupName
$($chapterTree -join "`r`n")
``````

## Working rule

Track pages own ordering. This course folder uses a stable reusable slug.

## Next step

Provide the curriculum and source material, then populate chapter guides one file at a time.
"@

Write-SafeFile `
    -Path (Join-Path $courseRoot 'README.md') `
    -Content $readme

$bom = @"
# Bill of Materials

## Course

- Title: $CourseName
- Canonical slug: ``$CourseSlug``
- Track: $TrackName
- Track position: $TrackPosition
- Status: Under construction

## Chapters

$($chapterSummary -join "`r`n")

## Source status

- Curriculum: pending
- Videos: pending
- Transcripts: pending
- Exercise notes: pending

## Planned artifacts

- Course landing page
- Accumulated Field Guide
- Chapter Field Guides
- Quick Lookup
- Lab Guide or light-lab note
- README
- Track link
- Course Library link
"@

Write-SafeFile `
    -Path (Join-Path $docsRoot 'BILL_OF_MATERIALS.md') `
    -Content $bom

$sourceReadme = @"
# Source Material

Place course evidence here:

- curriculum screenshots or notes
- raw transcripts
- lesson notes
- exercise notes
- archived source references

Raw sources are evidence. Final study content belongs under ``study_pages``.
"@

Write-SafeFile `
    -Path (Join-Path $sourceRoot 'README.md') `
    -Content $sourceReadme

Write-Host ''
Write-Host 'Course scaffold complete.' -ForegroundColor Green
Write-Host "Course root: $courseRoot"
Write-Host "Open:        $(Join-Path $courseRoot 'index.html')"
Write-Host 'No Git operations were performed.' -ForegroundColor DarkYellow
