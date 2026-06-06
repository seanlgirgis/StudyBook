$ProjectRoot = "D:\Workarea\StudyBook\study_maps\DataCamp\projects\analyzing_students_mental_health"

$Folders = @(
    $ProjectRoot
    "$ProjectRoot\docs"
    "$ProjectRoot\source_material"
    "$ProjectRoot\study_pages"
    "$ProjectRoot\lab"
    "$ProjectRoot\lab\sql"
    "$ProjectRoot\lab\expected_outputs"
    "$ProjectRoot\lab\notes"
)

foreach ($Folder in $Folders) {
    New-Item -ItemType Directory -Path $Folder -Force | Out-Null
}

$Files = @(
    "$ProjectRoot\index.html"
    "$ProjectRoot\README.md"
    "$ProjectRoot\docs\PROJECT_SETUP_AUDIT.md"
    "$ProjectRoot\source_material\README.md"
    "$ProjectRoot\study_pages\project_field_guide.html"
    "$ProjectRoot\study_pages\sql_quick_lookup.html"
    "$ProjectRoot\lab\lab_guide.html"
    "$ProjectRoot\lab\sql\00_create_students_table.sql"
    "$ProjectRoot\lab\sql\01_project_solution.sql"
    "$ProjectRoot\lab\sql\02_practice_queries.sql"
    "$ProjectRoot\lab\expected_outputs\README.md"
    "$ProjectRoot\lab\notes\troubleshooting.md"
)

foreach ($File in $Files) {
    if (-not (Test-Path $File)) {
        New-Item -ItemType File -Path $File | Out-Null
    }
}

Write-Host ""
Write-Host "Project scaffold created:"
Write-Host $ProjectRoot
Write-Host ""
Get-ChildItem -Path $ProjectRoot -Recurse
