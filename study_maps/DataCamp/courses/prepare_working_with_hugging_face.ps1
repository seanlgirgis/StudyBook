[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$CourseRoot = 'D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_hugging_face'
)

$ErrorActionPreference = 'Stop'

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Replace-InTextFile {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [object[]]$Replacements
    )

    $content = Get-Content -LiteralPath $Path -Raw
    $original = $content

    foreach ($entry in $Replacements) {
        $content = $content.Replace([string]$entry.From, [string]$entry.To)
    }

    if ($content -ne $original) {
        if ($PSCmdlet.ShouldProcess($Path, 'Update Hugging Face scaffold references')) {
            Set-Content -LiteralPath $Path -Value $content -Encoding utf8
        }
        return $true
    }

    return $false
}

if (-not (Test-Path -LiteralPath $CourseRoot -PathType Container)) {
    throw "Course folder not found: $CourseRoot"
}

$StudyPages = Join-Path $CourseRoot 'study_pages'
$LabRoot = Join-Path $CourseRoot 'lab'

if (-not (Test-Path -LiteralPath $StudyPages -PathType Container)) {
    throw "Study pages folder not found: $StudyPages"
}

Write-Step 'Normalize the quick-lookup filename'
$OldLookup = Join-Path $StudyPages 'sql_quick_lookup.html'
$NewLookup = Join-Path $StudyPages 'hugging_face_quick_lookup.html'

if (Test-Path -LiteralPath $OldLookup -PathType Leaf) {
    if (Test-Path -LiteralPath $NewLookup -PathType Leaf) {
        Write-Warning "Both quick-lookup files exist. No rename was performed.`nOld: $OldLookup`nNew: $NewLookup"
    }
    elseif ($PSCmdlet.ShouldProcess($OldLookup, "Rename to $(Split-Path $NewLookup -Leaf)")) {
        Rename-Item -LiteralPath $OldLookup -NewName (Split-Path $NewLookup -Leaf)
        Write-Host "Renamed: sql_quick_lookup.html -> hugging_face_quick_lookup.html" -ForegroundColor Green
    }
}
elseif (Test-Path -LiteralPath $NewLookup -PathType Leaf) {
    Write-Host 'Quick-lookup filename is already normalized.' -ForegroundColor DarkGreen
}
else {
    Write-Warning 'No quick-lookup HTML file was found. Intake can continue, but the lookup shell is missing.'
}

Write-Step 'Normalize quick-lookup labels and links'
$replacements = @(
    [pscustomobject]@{ From = 'sql_quick_lookup.html';     To = 'hugging_face_quick_lookup.html' }
    [pscustomobject]@{ From = 'SQL Join Quick Lookup';     To = 'Hugging Face Quick Lookup' }
    [pscustomobject]@{ From = 'Open SQL Quick Lookup';     To = 'Open Hugging Face Quick Lookup' }
    [pscustomobject]@{ From = 'SQL Quick Lookup';          To = 'Hugging Face Quick Lookup' }
    [pscustomobject]@{ From = 'SQL QUICK LOOKUP TEMPLATE'; To = 'HUGGING FACE QUICK LOOKUP TEMPLATE' }
    [pscustomobject]@{ From = 'SQL Quick Reference';       To = 'Hugging Face Quick Reference' }
    [pscustomobject]@{ From = 'SQL Quick Lookup Template'; To = 'Hugging Face Quick Lookup Template' }
)

$textFiles = Get-ChildItem -LiteralPath $CourseRoot -Recurse -File |
    Where-Object { $_.Extension -in '.html', '.md', '.txt' }

$changedFiles = New-Object System.Collections.Generic.List[string]
foreach ($file in $textFiles) {
    if (Replace-InTextFile -Path $file.FullName -Replacements $replacements) {
        $changedFiles.Add($file.FullName)
    }
}

Write-Step 'Normalize the course-local lab language folder'
$SqlLab = Join-Path $LabRoot 'sql'
$PythonLab = Join-Path $LabRoot 'python'

if (-not (Test-Path -LiteralPath $LabRoot -PathType Container)) {
    if ($PSCmdlet.ShouldProcess($LabRoot, 'Create lab folder')) {
        New-Item -ItemType Directory -Path $LabRoot | Out-Null
    }
}

if (Test-Path -LiteralPath $SqlLab -PathType Container) {
    $sqlItems = @(Get-ChildItem -LiteralPath $SqlLab -Force)

    if ($sqlItems.Count -eq 0 -and -not (Test-Path -LiteralPath $PythonLab)) {
        if ($PSCmdlet.ShouldProcess($SqlLab, 'Rename empty sql folder to python')) {
            Rename-Item -LiteralPath $SqlLab -NewName 'python'
            Write-Host 'Renamed empty lab\sql folder to lab\python.' -ForegroundColor Green
        }
    }
    elseif ($sqlItems.Count -gt 0) {
        Write-Warning 'lab\sql is not empty. It was preserved to avoid moving real files automatically.'
        if (-not (Test-Path -LiteralPath $PythonLab)) {
            if ($PSCmdlet.ShouldProcess($PythonLab, 'Create python lab folder')) {
                New-Item -ItemType Directory -Path $PythonLab | Out-Null
            }
        }
    }
}
elseif (-not (Test-Path -LiteralPath $PythonLab)) {
    if ($PSCmdlet.ShouldProcess($PythonLab, 'Create python lab folder')) {
        New-Item -ItemType Directory -Path $PythonLab | Out-Null
        Write-Host 'Created lab\python.' -ForegroundColor Green
    }
}
else {
    Write-Host 'lab\python already exists.' -ForegroundColor DarkGreen
}

$labPathReplacements = @(
    [pscustomobject]@{ From = 'lab\sql\'; To = 'lab\python\' }
    [pscustomobject]@{ From = 'lab/sql/'; To = 'lab/python/' }
    [pscustomobject]@{ From = 'lab\sql';  To = 'lab\python' }
    [pscustomobject]@{ From = 'lab/sql';  To = 'lab/python' }
)

foreach ($file in $textFiles) {
    if (Replace-InTextFile -Path $file.FullName -Replacements $labPathReplacements) {
        if (-not $changedFiles.Contains($file.FullName)) {
            $changedFiles.Add($file.FullName)
        }
    }
}

Write-Step 'Summary'
Write-Host "Course root: $CourseRoot"
Write-Host "Text files changed: $($changedFiles.Count)"
foreach ($path in $changedFiles) {
    Write-Host "  - $path"
}

Write-Host "`nScaffold normalization is complete. The course is ready for Chapter 1 intake." -ForegroundColor Green
