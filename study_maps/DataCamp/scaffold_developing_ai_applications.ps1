[CmdletBinding()]
param(
    [string]$DataCampRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp',
    [string]$TrackFolder = 'developing_ai_applications',
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function New-DirectorySafe {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created directory: $Path"
    }
}

function Write-TextFileSafe {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )
    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        Write-Host "Preserved existing file: $Path"
        return
    }
    $parent = Split-Path -Parent $Path
    if ($parent) { New-DirectorySafe -Path $parent }
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Host "Created file: $Path"
}

function Copy-TemplateSafe {
    param(
        [Parameter(Mandatory)][string]$TemplatePath,
        [Parameter(Mandatory)][string]$DestinationPath
    )
    if (-not (Test-Path -LiteralPath $TemplatePath)) {
        throw "Required template not found: $TemplatePath"
    }
    if ((Test-Path -LiteralPath $DestinationPath) -and -not $Force) {
        Write-Host "Preserved existing file: $DestinationPath"
        return
    }
    $parent = Split-Path -Parent $DestinationPath
    if ($parent) { New-DirectorySafe -Path $parent }
    Copy-Item -LiteralPath $TemplatePath -Destination $DestinationPath -Force
    Write-Host "Copied template: $DestinationPath"
}

function ConvertTo-Slug {
    param([Parameter(Mandatory)][string]$Text)
    $slug = $Text.ToLowerInvariant()
    $slug = [regex]::Replace($slug, '[^a-z0-9]+', '_')
    return $slug.Trim('_')
}

function New-MarkdownStub {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Body
    )
    $content = @"
# $Title

$Body
"@
    Write-TextFileSafe -Path $Path -Content $content
}

function New-CourseScaffold {
    param(
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Slug,
        [Parameter(Mandatory)][string[]]$Chapters,
        [Parameter(Mandatory)][int]$TrackPosition
    )

    $courseRoot = Join-Path $DataCampRoot "courses\$Slug"
    $dirs = @(
        $courseRoot,
        (Join-Path $courseRoot 'docs'),
        (Join-Path $courseRoot 'source_material'),
        (Join-Path $courseRoot 'source_material\archive'),
        (Join-Path $courseRoot 'study_pages'),
        (Join-Path $courseRoot 'lab'),
        (Join-Path $courseRoot 'lab\sql'),
        (Join-Path $courseRoot 'lab\expected_outputs'),
        (Join-Path $courseRoot 'lab\notes'),
        (Join-Path $courseRoot 'lab\source_archive')
    )
    $dirs | ForEach-Object { New-DirectorySafe -Path $_ }

    Copy-TemplateSafe -TemplatePath $courseIndexTemplate -DestinationPath (Join-Path $courseRoot 'index.html')
    Copy-TemplateSafe -TemplatePath $fieldGuideTemplate -DestinationPath (Join-Path $courseRoot 'study_pages\field_guide.html')
    Copy-TemplateSafe -TemplatePath $quickLookupTemplate -DestinationPath (Join-Path $courseRoot 'study_pages\sql_quick_lookup.html')

    for ($i = 0; $i -lt $Chapters.Count; $i++) {
        $number = '{0:D2}' -f ($i + 1)
        $chapterSlug = ConvertTo-Slug $Chapters[$i]
        $chapterFile = "chapter_${number}_${chapterSlug}_field_guide.html"
        Copy-TemplateSafe -TemplatePath $sectionGuideTemplate -DestinationPath (Join-Path $courseRoot "study_pages\$chapterFile")
    }

    $courseReadmeBody = @(
        'Canonical DataCamp course package for **Developing AI Applications**.',
        '',
        "- Track position: $TrackPosition",
        "- Canonical slug: ``$Slug``",
        '- Status: scaffolded; course content not yet studied'
    ) -join "`r`n"
    New-MarkdownStub -Path (Join-Path $courseRoot 'README.md') -Title $Title -Body $courseReadmeBody

    New-MarkdownStub -Path (Join-Path $courseRoot 'STUDYBUBBLE_SESSION_STATE.md') -Title "$Title - Session State" -Body 'Status: scaffolded. No course-completion or mastery claim has been made.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'docs\BILL_OF_MATERIALS.md') -Title "$Title - Bill of Materials" -Body 'Source inventory and coverage checklist will be populated during course intake.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'docs\COURSE_SETUP_AUDIT.md') -Title "$Title - Course Setup Audit" -Body 'Initial directory and template scaffold created. Placeholder replacement and navigation validation remain pending.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'source_material\README.md') -Title 'Source Material' -Body 'Place curriculum screenshots, transcripts, exercise notes, and source archives here.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'source_material\course_curriculum_outline.md') -Title "$Title - Curriculum Outline" -Body (($Chapters | ForEach-Object { "- $_" }) -join "`n")
    New-MarkdownStub -Path (Join-Path $courseRoot 'source_material\transcript_raw_combined.md') -Title "$Title - Raw Combined Transcript" -Body 'Transcript not yet supplied.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'source_material\exercise_notes.md') -Title "$Title - Exercise Notes" -Body 'Exercise notes will be captured during the live course pass.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'study_pages\field_guide.md') -Title "$Title - Field Guide" -Body 'Whole-course memory map. Populate chapter by chapter.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'lab\README.md') -Title "$Title - Lab" -Body 'Course-local practice area. Add runnable files only when justified by the course.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'lab\00_how_to_run.md') -Title 'How to Run the Lab' -Body 'Environment and run instructions are pending.'
    New-MarkdownStub -Path (Join-Path $courseRoot 'lab\lab_run_book.md') -Title "$Title - Lab Run Book" -Body 'Practice plan and observed evidence will be recorded here.'
}

function New-ProjectScaffold {
    param(
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Slug,
        [Parameter(Mandatory)][int]$TrackPosition
    )

    $projectRoot = Join-Path $DataCampRoot "projects\$Slug"
    $dirs = @(
        $projectRoot,
        (Join-Path $projectRoot 'docs'),
        (Join-Path $projectRoot 'source_material'),
        (Join-Path $projectRoot 'source_material\archive'),
        (Join-Path $projectRoot 'study_pages'),
        (Join-Path $projectRoot 'lab'),
        (Join-Path $projectRoot 'lab\sql'),
        (Join-Path $projectRoot 'lab\expected_outputs'),
        (Join-Path $projectRoot 'lab\notes')
    )
    $dirs | ForEach-Object { New-DirectorySafe -Path $_ }

    $projectReadmeBody = @(
        'Canonical DataCamp project package for **Developing AI Applications**.',
        '',
        "- Track position: $TrackPosition",
        "- Canonical slug: ``$Slug``",
        '- Status: scaffolded; project not yet completed'
    ) -join "`r`n"
    New-MarkdownStub -Path (Join-Path $projectRoot 'README.md') -Title $Title -Body $projectReadmeBody
    New-MarkdownStub -Path (Join-Path $projectRoot 'docs\PROJECT_SETUP_AUDIT.md') -Title "$Title - Project Setup Audit" -Body 'Initial scaffold created. Source intake, implementation, validation, and navigation remain pending.'
    New-MarkdownStub -Path (Join-Path $projectRoot 'source_material\README.md') -Title 'Source Material' -Body 'Place project instructions, datasets, screenshots, and source evidence here.'
    New-MarkdownStub -Path (Join-Path $projectRoot 'lab\README.md') -Title "$Title - Lab" -Body 'Runnable project reconstruction belongs here.'
    New-MarkdownStub -Path (Join-Path $projectRoot 'lab\lab_run_book.md') -Title "$Title - Lab Run Book" -Body 'Record implementation steps, outputs, errors, and corrections.'

    $projectHtml = @"
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>$Title</title></head>
<body>
<main>
  <h1>$Title</h1>
  <p>DataCamp project scaffold. Content and validation are pending.</p>
  <nav>
    <a href="../../skill_tracks/$TrackFolder/index.html">Developing AI Applications Track</a> |
    <a href="../../projects/index.html">Project Library</a> |
    <a href="../../index.html">DataCamp Home</a>
  </nav>
</main>
</body>
</html>
"@
    Write-TextFileSafe -Path (Join-Path $projectRoot 'index.html') -Content $projectHtml
    Write-TextFileSafe -Path (Join-Path $projectRoot 'study_pages\project_field_guide.html') -Content $projectHtml
    Write-TextFileSafe -Path (Join-Path $projectRoot 'study_pages\ai_quick_lookup.html') -Content $projectHtml
    Write-TextFileSafe -Path (Join-Path $projectRoot 'lab\lab_guide.html') -Content $projectHtml
}

# Validate roots and templates.
New-DirectorySafe -Path $DataCampRoot
$templateRoot = Join-Path $DataCampRoot 'Course_starter'
$courseIndexTemplate = Join-Path $templateRoot 'course_index_template.html'
$fieldGuideTemplate = Join-Path $templateRoot 'field_guide_template.html'
$sectionGuideTemplate = Join-Path $templateRoot 'section_field_guide_template.html'
$quickLookupTemplate = Join-Path $templateRoot 'sql_quick_lookup_template.html'

@($courseIndexTemplate, $fieldGuideTemplate, $sectionGuideTemplate, $quickLookupTemplate) | ForEach-Object {
    if (-not (Test-Path -LiteralPath $_)) {
        throw "Required authoritative template is missing: $_"
    }
}

$courses = @(
    [pscustomobject]@{ Position = 1; Title = 'Working with the OpenAI API'; Slug = 'working_with_the_openai_api'; Chapters = @('Introduction to the OpenAI API','Prompting OpenAI Models','Building Conversations with the OpenAI API') },
    [pscustomobject]@{ Position = 3; Title = 'AI Ethics'; Slug = 'ai_ethics'; Chapters = @('Approaching AI Ethics','Below the Surface: AI Ethics','The Way Forward: AI Ethics') },
    [pscustomobject]@{ Position = 4; Title = 'Prompt Engineering with the OpenAI API'; Slug = 'prompt_engineering_with_the_openai_api'; Chapters = @('Introduction to Prompt Engineering Best Practices','Advanced Prompt Engineering Strategies','Prompt Engineering for Business Applications','Prompt Engineering for Chatbot Development') },
    [pscustomobject]@{ Position = 5; Title = 'Working with Hugging Face'; Slug = 'working_with_hugging_face'; Chapters = @('Getting Started with Hugging Face','Building Pipelines with Hugging Face') },
    [pscustomobject]@{ Position = 6; Title = 'Introduction to Data Privacy'; Slug = 'introduction_to_data_privacy'; Chapters = @('Privacy Foundations','Privacy by Design','Living on the Edge') },
    [pscustomobject]@{ Position = 7; Title = 'Developing AI Systems with the OpenAI API'; Slug = 'developing_ai_systems_with_the_openai_api'; Chapters = @('Structuring End-to-End Applications','Function Calling','Best Practices for Production Applications') },
    [pscustomobject]@{ Position = 8; Title = 'Introduction to Embeddings with the OpenAI API'; Slug = 'introduction_to_embeddings_with_the_openai_api'; Chapters = @('What are Embeddings?','Embeddings for AI Applications','Vector Databases') },
    [pscustomobject]@{ Position = 10; Title = 'Developing LLM Applications with LangChain'; Slug = 'developing_llm_applications_with_langchain'; Chapters = @('Introduction to LangChain and Chatbot Mechanics','Chains and Agents','Retrieval Augmented Generation (RAG)') }
)

$projects = @(
    [pscustomobject]@{ Position = 2; Title = 'Planning a Trip to Paris with the OpenAI API'; Slug = 'planning_a_trip_to_paris_with_the_openai_api' },
    [pscustomobject]@{ Position = 9; Title = 'Topic Analysis of Clothing Reviews with Embeddings'; Slug = 'topic_analysis_of_clothing_reviews_with_embeddings' }
)

# Track container.
$trackRoot = Join-Path $DataCampRoot "skill_tracks\$TrackFolder"
New-DirectorySafe -Path $trackRoot
New-DirectorySafe -Path (Join-Path $trackRoot 'docs')

$trackItems = @(
    [pscustomobject]@{ Position = 1; Type = 'Course'; Title = 'Working with the OpenAI API'; Href = '../../courses/working_with_the_openai_api/index.html' },
    [pscustomobject]@{ Position = 2; Type = 'Project'; Title = 'Planning a Trip to Paris with the OpenAI API'; Href = '../../projects/planning_a_trip_to_paris_with_the_openai_api/index.html' },
    [pscustomobject]@{ Position = 3; Type = 'Course'; Title = 'AI Ethics'; Href = '../../courses/ai_ethics/index.html' },
    [pscustomobject]@{ Position = 4; Type = 'Course'; Title = 'Prompt Engineering with the OpenAI API'; Href = '../../courses/prompt_engineering_with_the_openai_api/index.html' },
    [pscustomobject]@{ Position = 5; Type = 'Course'; Title = 'Working with Hugging Face'; Href = '../../courses/working_with_hugging_face/index.html' },
    [pscustomobject]@{ Position = 6; Type = 'Course'; Title = 'Introduction to Data Privacy'; Href = '../../courses/introduction_to_data_privacy/index.html' },
    [pscustomobject]@{ Position = 7; Type = 'Course'; Title = 'Developing AI Systems with the OpenAI API'; Href = '../../courses/developing_ai_systems_with_the_openai_api/index.html' },
    [pscustomobject]@{ Position = 8; Type = 'Course'; Title = 'Introduction to Embeddings with the OpenAI API'; Href = '../../courses/introduction_to_embeddings_with_the_openai_api/index.html' },
    [pscustomobject]@{ Position = 9; Type = 'Project'; Title = 'Topic Analysis of Clothing Reviews with Embeddings'; Href = '../../projects/topic_analysis_of_clothing_reviews_with_embeddings/index.html' },
    [pscustomobject]@{ Position = 10; Type = 'Course'; Title = 'Developing LLM Applications with LangChain'; Href = '../../courses/developing_llm_applications_with_langchain/index.html' }
)

$cards = ($trackItems | ForEach-Object {
@"
        <article class="card">
          <span class="badge">$($_.Type) $($_.Position)</span>
          <h2><a href="$($_.Href)">$($_.Title)</a></h2>
          <p>Scaffolded canonical package. Study content and completion evidence are pending.</p>
        </article>
"@
}) -join "`n"

$trackIndex = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Developing AI Applications | DataCamp StudyBook</title>
  <style>
    :root{--bg:#0d1117;--panel:#161b22;--border:#30363d;--text:#e6edf3;--muted:#9da7b3;--green:#03ef62;--blue:#58a6ff}
    *{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
    .page{width:min(1120px,calc(100% - 32px));margin:auto;padding:24px 0 48px}.hero,.card{background:var(--panel);border:1px solid var(--border);border-radius:14px}
    .hero{padding:30px;border-top:5px solid var(--green)}h1{margin:0;font-size:clamp(2rem,4vw,3rem)}.hero p,.card p{color:var(--muted)}
    nav{margin:16px 0}a{color:var(--blue);text-decoration:none}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:22px}
    .card{padding:18px}.card h2{font-size:1.08rem;margin:8px 0}.badge{display:inline-block;padding:4px 8px;border-radius:999px;background:rgba(3,239,98,.12);color:var(--green);font-weight:800;font-size:.78rem}
    @media(max-width:720px){.grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
<main class="page">
  <nav><a href="../index.html">Skill Tracks</a> | <a href="../../index.html">DataCamp Home</a> | <a href="../../courses/index.html">Course Library</a> | <a href="../../projects/index.html">Project Library</a></nav>
  <header class="hero">
    <p>DATACAMP SKILL TRACK</p>
    <h1>Developing AI Applications</h1>
    <p>Track scaffold for OpenAI API development, prompt engineering, Hugging Face, privacy, embeddings, vector databases, LangChain, and retrieval-augmented generation.</p>
    <p><strong>Status:</strong> Structure ready | learning not started</p>
  </header>
  <section class="grid">
$cards
  </section>
</main>
</body>
</html>
"@
Write-TextFileSafe -Path (Join-Path $trackRoot 'index.html') -Content $trackIndex

New-MarkdownStub -Path (Join-Path $trackRoot 'README.md') -Title 'Developing AI Applications' -Body 'This track owns ordering and links. Courses and projects remain canonical reusable packages under the shared course and project libraries.'
New-MarkdownStub -Path (Join-Path $trackRoot 'docs\TRACK_SETUP_AUDIT.md') -Title 'Developing AI Applications - Track Setup Audit' -Body 'Track scaffold created. Main DataCamp landing-page wiring and library-card updates require the current live index files and remain pending.'
New-MarkdownStub -Path (Join-Path $trackRoot 'TRACK_STATE.md') -Title 'Developing AI Applications - Track State' -Body 'Structure ready. No course or project completion claims have been made.'

foreach ($course in $courses) {
    New-CourseScaffold -Title $course.Title -Slug $course.Slug -Chapters $course.Chapters -TrackPosition $course.Position
}
foreach ($project in $projects) {
    New-ProjectScaffold -Title $project.Title -Slug $project.Slug -TrackPosition $project.Position
}

$manifestLines = @(
    '# Developing AI Applications - Scaffold Manifest',
    '',
    "Track folder: ``skill_tracks\$TrackFolder``",
    '',
    '## Ordered items'
)
foreach ($item in $trackItems) {
    $manifestLines += "- $($item.Position). [$($item.Type)] $($item.Title)"
}
$manifestLines += @(
    '',
    '## Deliberately not modified',
    '',
    '- `DataCamp\index.html`',
    '- `DataCamp\skill_tracks\index.html`',
    '- `DataCamp\courses\index.html`',
    '- `DataCamp\projects\index.html`',
    '',
    'Those live navigation pages should be updated only from their current files so existing design and links are preserved.'
)
Write-TextFileSafe -Path (Join-Path $trackRoot 'SCAFFOLD_MANIFEST.md') -Content ($manifestLines -join "`r`n")

Write-Host ''
Write-Host 'Developing AI Applications scaffold complete.' -ForegroundColor Green
Write-Host "Track page: $(Join-Path $trackRoot 'index.html')"
Write-Host 'Next safe step: provide the current DataCamp root, skill-track library, course library, and project library index files for exact navigation updates.'
