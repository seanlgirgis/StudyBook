$courseRoot = "D:\Workarea\StudyBook\study_maps\DataCamp\courses\intermediate_sql"

# Create folders
$folders = @(
    $courseRoot
    "$courseRoot\docs"
    "$courseRoot\source_material"
    "$courseRoot\source_material\archive"
    "$courseRoot\study_pages"
    "$courseRoot\lab"
    "$courseRoot\lab\sql"
    "$courseRoot\lab\expected_outputs"
    "$courseRoot\lab\notes"
    "$courseRoot\lab\source_archive"
)

$folders | ForEach-Object {
    New-Item -ItemType Directory -Path $_ -Force | Out-Null
}

# Create empty stub files
$files = @(
    "$courseRoot\index.html"
    "$courseRoot\README.md"
    "$courseRoot\STUDYBUBBLE_SESSION_STATE.md"

    "$courseRoot\docs\BILL_OF_MATERIALS.md"
    "$courseRoot\docs\COURSE_SETUP_AUDIT.md"

    "$courseRoot\source_material\README.md"
    "$courseRoot\source_material\course_curriculum_outline.md"
    "$courseRoot\source_material\transcript_raw_combined.md"
    "$courseRoot\source_material\exercise_notes.md"

    "$courseRoot\study_pages\field_guide.md"
    "$courseRoot\study_pages\field_guide.html"
    "$courseRoot\study_pages\sql_quick_lookup.html"

    "$courseRoot\lab\README.md"
    "$courseRoot\lab\00_how_to_run.md"
    "$courseRoot\lab\lab_run_book.md"
    "$courseRoot\lab\expected_outputs\README.md"
    "$courseRoot\lab\notes\troubleshooting.md"
    "$courseRoot\study_pages\chapter_01_selecting_data_field_guide.html"
    "$courseRoot\study_pages\chapter_02_filtering_records_field_guide.html"
    "$courseRoot\study_pages\chapter_03_aggregate_functions_field_guide.html"
    "$courseRoot\study_pages\chapter_04_sorting_and_grouping_field_guide.html"
)

$files | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType File -Path $_ | Out-Null
    }
}

Write-Host "Intermediate SQL course shell created at:"
Write-Host $courseRoot