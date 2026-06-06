[CmdletBinding()]
param(
    [string]$StudyBookRoot = 'D:\Workarea\StudyBook',
    [string]$CourseSlug = 'postgresql_summary_stats_and_window_functions',
    [string]$SourceCsv = '',
    [string]$CoursePdf = '',
    [string]$CourseImage = '',
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Info([string]$Message) {
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Ok([string]$Message) {
    Write-Host "[ OK ] $Message" -ForegroundColor Green
}

function Write-Skip([string]$Message) {
    Write-Host "[SKIP] $Message" -ForegroundColor Yellow
}

function Ensure-Directory([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Ok "Created directory: $Path"
    }
}

function Write-TextFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        Write-Skip "Exists: $Path"
        return
    }

    $parent = Split-Path -Parent $Path
    Ensure-Directory $parent
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Ok "Wrote: $Path"
}

function Copy-OptionalSource {
    param(
        [string]$Source,
        [string]$DestinationDirectory
    )

    if ([string]::IsNullOrWhiteSpace($Source)) {
        return
    }

    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        Write-Warning "Source file not found: $Source"
        return
    }

    Ensure-Directory $DestinationDirectory
    $destination = Join-Path $DestinationDirectory (Split-Path -Leaf $Source)

    if ((Test-Path -LiteralPath $destination) -and -not $Force) {
        Write-Skip "Source already copied: $destination"
        return
    }

    Copy-Item -LiteralPath $Source -Destination $destination -Force
    Write-Ok "Copied source: $destination"
}

$DataCampRoot = Join-Path $StudyBookRoot 'study_maps\DataCamp'
$CourseRoot = Join-Path $DataCampRoot "courses\$CourseSlug"
$DocsRoot = Join-Path $CourseRoot 'docs'
$SourceRoot = Join-Path $CourseRoot 'source_material'
$SourceArchive = Join-Path $SourceRoot 'archive'
$StudyPagesRoot = Join-Path $CourseRoot 'study_pages'
$LabRoot = Join-Path $CourseRoot 'lab'
$LabSqlRoot = Join-Path $LabRoot 'sql'
$LabDataRoot = Join-Path $LabRoot 'data'
$LabExpectedRoot = Join-Path $LabRoot 'expected_outputs'
$LabNotesRoot = Join-Path $LabRoot 'notes'
$LabSourceArchive = Join-Path $LabRoot 'source_archive'

Write-Info "Creating course package at: $CourseRoot"

@(
    $CourseRoot,
    $DocsRoot,
    $SourceRoot,
    $SourceArchive,
    $StudyPagesRoot,
    $LabRoot,
    $LabSqlRoot,
    $LabDataRoot,
    $LabExpectedRoot,
    $LabNotesRoot,
    $LabSourceArchive
) | ForEach-Object { Ensure-Directory $_ }

$readme = @'
# PostgreSQL Summary Stats and Window Functions

Canonical DataCamp course package.

## Course status

- Platform status: Complete
- Documentation coverage: In progress
- Lab coverage: Developing
- Recall confidence: Needs review
- Interview readiness: Needs repetition

## Main artifacts

- `index.html` — course front door
- `study_pages/field_guide.md` — accumulated course guide
- `study_pages/field_guide.html` — browser field guide
- `study_pages/chapter_01_introduction_to_window_functions_field_guide.html`
- `study_pages/chapter_02_fetching_ranking_and_paging_field_guide.html`
- `study_pages/chapter_03_aggregate_window_functions_and_frames_field_guide.html`
- `study_pages/chapter_04_beyond_window_functions_field_guide.html`
- `study_pages/sql_quick_lookup.html`
- `lab/lab_run_book.md`
- `lab/sql/` — runnable PostgreSQL practice

## Dataset

The course lab uses the Summer Olympics dataset when `summer.csv` is supplied to the bootstrap script.
'@
Write-TextFile (Join-Path $CourseRoot 'README.md') $readme

$sessionState = @'
# StudyBubble Session State

## Course

PostgreSQL Summary Stats and Window Functions

## Current state

- DataCamp platform course completed.
- Four chapters identified.
- Canonical course-local lab structure created.
- Summer Olympics CSV may be loaded into PostgreSQL for practice.

## Next work

1. Populate chapter field guides from completed exercises.
2. Reconcile the accumulated field guide.
3. Run the SQL lab scripts.
4. Record observed outputs and mistakes.
5. Update DataCamp course and track navigation.
'@
Write-TextFile (Join-Path $CourseRoot 'STUDYBUBBLE_SESSION_STATE.md') $sessionState

$bom = @'
# Bill of Materials

## Course identity

- Title: PostgreSQL Summary Stats and Window Functions
- Canonical slug: `postgresql_summary_stats_and_window_functions`
- Level: Intermediate
- Platform status: Complete
- Duration shown: 4 hours
- Videos shown: 12
- Exercises shown: 44

## Chapters

1. Introduction to window functions
2. Fetching, ranking, and paging
3. Aggregate window functions and frames
4. Beyond window functions

## Core topics

- `OVER()`
- `PARTITION BY`
- `ORDER BY` within `OVER()`
- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `LAG()` and `LEAD()`
- `FIRST_VALUE()` and `LAST_VALUE()`
- Aggregate window functions
- Running totals
- Moving averages
- `ROWS BETWEEN`
- `RANGE BETWEEN`
- `NTILE()`
- CTEs
- `ROLLUP` and `CUBE`
- `STRING_AGG()`
- PostgreSQL `tablefunc` / `CROSSTAB()`

## Sources

- Course screenshot/image: optional source archive
- Course glossary PDF: optional source archive
- `summer.csv`: lab dataset

## Target artifacts

- Accumulated Field Guide Markdown and HTML
- Four chapter field guides
- SQL Quick Lookup
- Lab Run Book
- SQL setup, loading, and practice scripts
- Expected-output notes
- Troubleshooting notes
'@
Write-TextFile (Join-Path $DocsRoot 'BILL_OF_MATERIALS.md') $bom

$audit = @'
# Course Setup Audit

## Expected canonical path

`study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions`

## Setup checks

- [x] Course front door exists
- [x] README exists
- [x] Session state exists
- [x] Bill of Materials exists
- [x] Source archive exists
- [x] Study-pages folder exists
- [x] Course-local lab folder exists
- [x] SQL folder exists
- [x] Expected-output folder exists
- [x] Troubleshooting folder exists
- [ ] Chapter guides populated
- [ ] Accumulated guide reconciled
- [ ] Lab executed successfully
- [ ] Navigation indexes updated
'@
Write-TextFile (Join-Path $DocsRoot 'COURSE_SETUP_AUDIT.md') $audit

$sourceReadme = @'
# Source Material

This folder preserves course evidence such as curriculum screenshots, glossary PDFs, transcripts, and exercise notes.

Raw source material is evidence, not the final study product.
'@
Write-TextFile (Join-Path $SourceRoot 'README.md') $sourceReadme

$outline = @'
# Course Curriculum Outline

## Chapter 1 — Introduction to window functions

Window-function foundations, `OVER()`, `ORDER BY`, and `PARTITION BY`.

## Chapter 2 — Fetching, ranking, and paging

Fetching values from other rows, ranking rows, and dividing ordered data into pages or tiles.

## Chapter 3 — Aggregate window functions and frames

Using familiar aggregates as window functions and controlling their row frames.

## Chapter 4 — Beyond window functions

Supporting PostgreSQL techniques used with analytical queries, including CTEs, subtotals, string aggregation, and pivoting.
'@
Write-TextFile (Join-Path $SourceRoot 'course_curriculum_outline.md') $outline
Write-TextFile (Join-Path $SourceRoot 'transcript_raw_combined.md') "# Raw Combined Transcript`r`n`r`nSource transcript not yet supplied."
Write-TextFile (Join-Path $SourceRoot 'exercise_notes.md') "# Exercise Notes`r`n`r`nCapture exercise prompts, solutions, mistakes, and corrections here."

$fieldGuideMd = @'
# PostgreSQL Summary Stats and Window Functions Field Guide

## Course map

1. Window-function foundations
2. Fetching and ranking
3. Aggregate windows and frames
4. Supporting analytical SQL techniques

## Core mental model

A window function calculates across related rows while preserving one result row for every input row.

## Essential pattern

```sql
function_expression OVER (
    PARTITION BY grouping_column
    ORDER BY ordering_column
    ROWS BETWEEN frame_start AND frame_end
)
```

## Chapter links

- [Chapter 1](chapter_01_introduction_to_window_functions_field_guide.html)
- [Chapter 2](chapter_02_fetching_ranking_and_paging_field_guide.html)
- [Chapter 3](chapter_03_aggregate_window_functions_and_frames_field_guide.html)
- [Chapter 4](chapter_04_beyond_window_functions_field_guide.html)
- [SQL Quick Lookup](sql_quick_lookup.html)
- [Lab Run Book](../lab/lab_run_book.md)

## Reusable interview sentence

Window functions let me calculate rankings, comparisons, running totals, and moving statistics across related rows without collapsing the detailed result set as `GROUP BY` would.
'@
Write-TextFile (Join-Path $StudyPagesRoot 'field_guide.md') $fieldGuideMd

function New-HtmlPage([string]$Title, [string]$Body) {
@"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$Title</title>
  <style>
    :root { color-scheme: dark; --bg:#0d1117; --panel:#161b22; --line:#30363d; --text:#e6edf3; --muted:#9da7b3; --accent:#58a6ff; --good:#3fb950; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:Arial,Helvetica,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }
    header { border-top:4px solid var(--accent); border-bottom:1px solid var(--line); background:#010409; }
    .container { width:min(1100px,92%); margin:auto; padding:28px 0; }
    .badge { display:inline-block; padding:4px 10px; border:1px solid var(--good); border-radius:999px; color:var(--good); font-size:.82rem; }
    nav, section { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:20px; margin:18px 0; }
    a { color:var(--accent); }
    code, pre { font-family:Consolas,monospace; }
    pre { overflow:auto; background:#010409; border:1px solid var(--line); border-radius:8px; padding:16px; }
    .muted { color:var(--muted); }
  </style>
</head>
<body>
<header><div class="container"><span class="badge">DataCamp Course</span><h1>$Title</h1></div></header>
<main class="container">
$Body
</main>
</body>
</html>
"@
}

$courseIndexBody = @'
<nav>
  <h2>Start here</h2>
  <ul>
    <li><a href="study_pages/field_guide.html">Accumulated Field Guide</a></li>
    <li><a href="study_pages/sql_quick_lookup.html">SQL Quick Lookup</a></li>
    <li><a href="lab/lab_guide.html">Hands-on Lab Guide</a></li>
  </ul>
</nav>
<section>
  <h2>Chapter guides</h2>
  <ol>
    <li><a href="study_pages/chapter_01_introduction_to_window_functions_field_guide.html">Introduction to window functions</a></li>
    <li><a href="study_pages/chapter_02_fetching_ranking_and_paging_field_guide.html">Fetching, ranking, and paging</a></li>
    <li><a href="study_pages/chapter_03_aggregate_window_functions_and_frames_field_guide.html">Aggregate window functions and frames</a></li>
    <li><a href="study_pages/chapter_04_beyond_window_functions_field_guide.html">Beyond window functions</a></li>
  </ol>
</section>
<section><h2>Status</h2><p>Platform complete. StudyBook documentation and lab practice are developing.</p></section>
'@
Write-TextFile (Join-Path $CourseRoot 'index.html') (New-HtmlPage 'PostgreSQL Summary Stats and Window Functions' $courseIndexBody)

$fieldGuideBody = @'
<nav><a href="../index.html">Course Home</a> | <a href="sql_quick_lookup.html">Quick Lookup</a> | <a href="../lab/lab_guide.html">Lab Guide</a></nav>
<section><h2>Core mental model</h2><p>A window function calculates over related rows while retaining every detail row.</p></section>
<section><h2>Essential syntax</h2><pre><code>function_expression OVER (
  PARTITION BY grouping_column
  ORDER BY ordering_column
  ROWS BETWEEN frame_start AND frame_end
)</code></pre></section>
<section><h2>Course chapters</h2><ol><li>Window foundations</li><li>Fetching, ranking, and paging</li><li>Aggregate windows and frames</li><li>Beyond window functions</li></ol></section>
<section><h2>Interview translation</h2><p>I use window functions for ranking, row-to-row comparisons, running totals, and moving statistics without collapsing detailed rows.</p></section>
'@
Write-TextFile (Join-Path $StudyPagesRoot 'field_guide.html') (New-HtmlPage 'PostgreSQL Window Functions Field Guide' $fieldGuideBody)

$chapters = @(
    @{ File='chapter_01_introduction_to_window_functions_field_guide.html'; Title='Chapter 1 — Introduction to Window Functions'; Focus='OVER(), ORDER BY within OVER(), and PARTITION BY' },
    @{ File='chapter_02_fetching_ranking_and_paging_field_guide.html'; Title='Chapter 2 — Fetching, Ranking, and Paging'; Focus='LAG, LEAD, ranking functions, and NTILE' },
    @{ File='chapter_03_aggregate_window_functions_and_frames_field_guide.html'; Title='Chapter 3 — Aggregate Window Functions and Frames'; Focus='SUM/AVG as windows, running totals, moving averages, ROWS and RANGE frames' },
    @{ File='chapter_04_beyond_window_functions_field_guide.html'; Title='Chapter 4 — Beyond Window Functions'; Focus='CTEs, ROLLUP, CUBE, STRING_AGG, and CROSSTAB' }
)

foreach ($chapter in $chapters) {
    $body = @(
        '<nav><a href="../index.html">Course Home</a> | <a href="field_guide.html">Field Guide</a> | <a href="sql_quick_lookup.html">Quick Lookup</a></nav>'
        "<section><h2>Chapter focus</h2><p>$($chapter.Focus)</p></section>"
        '<section><h2>Worked examples</h2><p class="muted">Populate during the live review pass.</p></section>'
        '<section><h2>Common mistakes</h2><p class="muted">Record mistakes and corrections here.</p></section>'
        '<section><h2>Interview Q&amp;A</h2><p class="muted">Add concise interview-safe answers here.</p></section>'
    ) -join [Environment]::NewLine
    Write-TextFile (Join-Path $StudyPagesRoot $chapter.File) (New-HtmlPage $chapter.Title $body)
}

$quickLookupBody = @'
<nav><a href="../index.html">Course Home</a> | <a href="field_guide.html">Field Guide</a> | <a href="../lab/lab_guide.html">Lab Guide</a></nav>
<section><h2>Ranking</h2><pre><code>ROW_NUMBER() OVER (ORDER BY value DESC)
RANK()       OVER (ORDER BY value DESC)
DENSE_RANK() OVER (ORDER BY value DESC)</code></pre></section>
<section><h2>Previous and next row</h2><pre><code>LAG(value)  OVER (PARTITION BY group_col ORDER BY time_col)
LEAD(value) OVER (PARTITION BY group_col ORDER BY time_col)</code></pre></section>
<section><h2>Running total</h2><pre><code>SUM(value) OVER (
  PARTITION BY group_col
  ORDER BY time_col
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)</code></pre></section>
<section><h2>Moving average</h2><pre><code>AVG(value) OVER (
  ORDER BY time_col
  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)</code></pre></section>
'@
Write-TextFile (Join-Path $StudyPagesRoot 'sql_quick_lookup.html') (New-HtmlPage 'SQL Window Functions Quick Lookup' $quickLookupBody)

$labReadme = @'
# Course Lab

This lab uses PostgreSQL and the Summer Olympics dataset.

## Run order

1. `sql/00_create_schema.sql`
2. `sql/01_create_tables.sql`
3. `sql/02_load_summer_data.sql`
4. `sql/03_window_function_practice.sql`
5. `sql/04_advanced_summary_practice.sql`

See `00_how_to_run.md` for commands.
'@
Write-TextFile (Join-Path $LabRoot 'README.md') $labReadme

$howToRun = @'
# How to Run the Lab

## Option A — run from psql

```powershell
cd D:\Workarea\StudyBook\study_maps\DataCamp\courses\postgresql_summary_stats_and_window_functions\lab
psql -U postgres -d studybook -f .\sql\00_create_schema.sql
psql -U postgres -d studybook -f .\sql\01_create_tables.sql
psql -U postgres -d studybook -f .\sql\02_load_summer_data.sql
psql -U postgres -d studybook -f .\sql\03_window_function_practice.sql
psql -U postgres -d studybook -f .\sql\04_advanced_summary_practice.sql
```

Change the PostgreSQL user or database if your local environment uses different values.

## Option B — from inside psql

```sql
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/00_create_schema.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/01_create_tables.sql'
\i 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/sql/02_load_summer_data.sql'
```
'@
Write-TextFile (Join-Path $LabRoot '00_how_to_run.md') $howToRun

$labRunBook = @'
# Lab Run Book

## Purpose

Practice summary statistics and PostgreSQL window functions against the Summer Olympics medal dataset.

## Checkpoints

- [ ] Create schema and table
- [ ] Load `summer.csv`
- [ ] Validate row count
- [ ] Rank athletes and countries
- [ ] Compare rows with LAG/LEAD
- [ ] Calculate running totals
- [ ] Calculate moving averages
- [ ] Divide results with NTILE
- [ ] Practice ROLLUP/CUBE
- [ ] Practice STRING_AGG
- [ ] Record mistakes and corrections

## Evidence

Record executed queries, observed outputs, and corrections below.
'@
Write-TextFile (Join-Path $LabRoot 'lab_run_book.md') $labRunBook

$labGuideBody = @'
<nav><a href="../index.html">Course Home</a> | <a href="../study_pages/field_guide.html">Field Guide</a> | <a href="../study_pages/sql_quick_lookup.html">Quick Lookup</a></nav>
<section><h2>Dataset</h2><p>Summer Olympics medal records with year, city, sport, discipline, athlete, country, gender, event, and medal.</p></section>
<section><h2>Run order</h2><ol><li>Create schema</li><li>Create table</li><li>Load CSV</li><li>Run window-function practice</li><li>Run advanced summary practice</li></ol></section>
<section><h2>Practice goals</h2><p>Ranking, paging, prior/next-row comparisons, running totals, moving averages, frames, subtotals, and string aggregation.</p></section>
'@
Write-TextFile (Join-Path $LabRoot 'lab_guide.html') (New-HtmlPage 'PostgreSQL Window Functions Lab Guide' $labGuideBody)

$createSchemaSql = @'
DROP SCHEMA IF EXISTS dc_window_functions CASCADE;
CREATE SCHEMA dc_window_functions;
SET search_path TO dc_window_functions, public;
'@
Write-TextFile (Join-Path $LabSqlRoot '00_create_schema.sql') $createSchemaSql

$createTablesSql = @'
SET search_path TO dc_window_functions, public;

CREATE TABLE IF NOT EXISTS summer_medals (
    medal_id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year        integer NOT NULL,
    city        text NOT NULL,
    sport       text NOT NULL,
    discipline  text NOT NULL,
    athlete     text NOT NULL,
    country     text,
    gender      text NOT NULL,
    event       text NOT NULL,
    medal       text NOT NULL,
    CONSTRAINT summer_medals_medal_check
        CHECK (medal IN ('Gold', 'Silver', 'Bronze'))
);

CREATE INDEX IF NOT EXISTS ix_summer_medals_year
    ON summer_medals (year);
CREATE INDEX IF NOT EXISTS ix_summer_medals_country_year
    ON summer_medals (country, year);
CREATE INDEX IF NOT EXISTS ix_summer_medals_athlete
    ON summer_medals (athlete);
'@
Write-TextFile (Join-Path $LabSqlRoot '01_create_tables.sql') $createTablesSql

$csvDestination = Join-Path $LabDataRoot 'summer.csv'
$csvForPsql = $csvDestination.Replace('\','/')
$loadSql = @"
SET search_path TO dc_window_functions, public;

TRUNCATE TABLE summer_medals RESTART IDENTITY;

\copy summer_medals (year, city, sport, discipline, athlete, country, gender, event, medal)
FROM '$csvForPsql'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

SELECT COUNT(*) AS loaded_rows FROM summer_medals;
"@
Write-TextFile (Join-Path $LabSqlRoot '02_load_summer_data.sql') $loadSql

$practiceSql = @'
SET search_path TO dc_window_functions, public;

-- 1. Number medals within each Olympic year.
SELECT
    year,
    athlete,
    country,
    medal,
    ROW_NUMBER() OVER (
        PARTITION BY year
        ORDER BY athlete, event, medal_id
    ) AS row_in_year
FROM summer_medals
ORDER BY year, row_in_year
LIMIT 50;

-- 2. Rank countries by Gold medals for each year.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    RANK() OVER (PARTITION BY year ORDER BY gold_medals DESC) AS medal_rank,
    DENSE_RANK() OVER (PARTITION BY year ORDER BY gold_medals DESC) AS dense_medal_rank
FROM country_gold
ORDER BY year, medal_rank, country;

-- 3. Compare each country's Gold medals with its previous Olympics.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    LAG(gold_medals) OVER (PARTITION BY country ORDER BY year) AS previous_gold_medals,
    gold_medals - LAG(gold_medals) OVER (PARTITION BY country ORDER BY year) AS change_from_previous
FROM country_gold
ORDER BY country, year;

-- 4. Running Gold-medal total by country.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    SUM(gold_medals) OVER (
        PARTITION BY country
        ORDER BY year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_gold_total
FROM country_gold
ORDER BY country, year;

-- 5. Three-Olympics moving average.
WITH country_gold AS (
    SELECT year, country, COUNT(*) AS gold_medals
    FROM summer_medals
    WHERE medal = 'Gold' AND country IS NOT NULL
    GROUP BY year, country
)
SELECT
    year,
    country,
    gold_medals,
    ROUND(
        AVG(gold_medals) OVER (
            PARTITION BY country
            ORDER BY year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS three_games_moving_avg
FROM country_gold
ORDER BY country, year;

-- 6. Divide athletes into four medal-count buckets.
WITH athlete_medals AS (
    SELECT athlete, COUNT(*) AS medal_count
    FROM summer_medals
    GROUP BY athlete
)
SELECT
    athlete,
    medal_count,
    NTILE(4) OVER (ORDER BY medal_count DESC, athlete) AS medal_quartile
FROM athlete_medals
ORDER BY medal_quartile, medal_count DESC, athlete;
'@
Write-TextFile (Join-Path $LabSqlRoot '03_window_function_practice.sql') $practiceSql

$advancedSql = @'
SET search_path TO dc_window_functions, public;

-- Hierarchical subtotals with ROLLUP.
SELECT
    year,
    country,
    COUNT(*) AS medal_count
FROM summer_medals
GROUP BY ROLLUP (year, country)
ORDER BY year NULLS LAST, country NULLS LAST;

-- All subtotal combinations with CUBE.
SELECT
    sport,
    medal,
    COUNT(*) AS medal_count
FROM summer_medals
GROUP BY CUBE (sport, medal)
ORDER BY sport NULLS LAST, medal NULLS LAST;

-- Compress event names into one row per sport.
SELECT
    sport,
    STRING_AGG(DISTINCT event, ', ' ORDER BY event) AS events
FROM summer_medals
GROUP BY sport
ORDER BY sport;

-- Optional pivot support.
CREATE EXTENSION IF NOT EXISTS tablefunc;
'@
Write-TextFile (Join-Path $LabSqlRoot '04_advanced_summary_practice.sql') $advancedSql

Write-TextFile (Join-Path $LabExpectedRoot 'README.md') "# Expected Outputs`r`n`r`nRecord validated row counts and representative query results here after running the lab."
Write-TextFile (Join-Path $LabNotesRoot 'troubleshooting.md') @'
# Troubleshooting

## `\copy` cannot find the CSV

Confirm that `lab/data/summer.csv` exists. Re-run the bootstrap script with `-SourceCsv` if needed.

## Permission denied for `CREATE EXTENSION`

Run the extension command as a PostgreSQL role with sufficient privileges, or skip the optional CROSSTAB exercise.

## Schema objects are not found

Run `00_create_schema.sql` and `01_create_tables.sql` first, and confirm the active database.
'@

Copy-OptionalSource -Source $SourceCsv -DestinationDirectory $LabDataRoot
Copy-OptionalSource -Source $CoursePdf -DestinationDirectory $SourceArchive
Copy-OptionalSource -Source $CourseImage -DestinationDirectory $SourceArchive

Write-Host ''
Write-Ok 'Course and lab scaffold created.'
Write-Host "Course home: $CourseRoot\index.html" -ForegroundColor White
Write-Host "Lab guide:   $LabRoot\lab_guide.html" -ForegroundColor White
Write-Host "Run guide:   $LabRoot\00_how_to_run.md" -ForegroundColor White

if (-not (Test-Path -LiteralPath $csvDestination)) {
    Write-Warning "summer.csv was not copied. Re-run with -SourceCsv '<full path to summer.csv>' before running 02_load_summer_data.sql."
}
