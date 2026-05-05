# init_04g_from_04f.ps1
# Purpose: Initialize pocs/04g folder with Phase 1 logic from 04f
# So 04f and 04g are sister folders for independent development

# Set base paths
$basePath = "D:\Workarea\StudyBook\demos\rag\pocs"
$source = Join-Path $basePath "04f"
$destination = Join-Path $basePath "04g"

# Create destination folder if it doesn't exist
if (-Not (Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
}

# Copy Phase 1 logic to 04g
# Include src/, data/, outputs/, config/, and interactive scripts
$foldersToCopy = @("src", "data", "outputs", "config")
foreach ($folder in $foldersToCopy) {
    $srcFolder = Join-Path $source $folder
    if (Test-Path $srcFolder) {
        $destFolder = Join-Path $destination $folder
        Copy-Item -Path $srcFolder -Destination $destFolder -Recurse -Force
    }
}

# Copy interactive CLI and test scripts
$scriptsToCopy = @("interactive_grok_test.py", "test_phase1_multisentence.py")
foreach ($script in $scriptsToCopy) {
    $srcFile = Join-Path $source $script
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $destination -Force
    }
}

# Feedback
Write-Host "04g initialized from 04f. Folders and scripts copied successfully."