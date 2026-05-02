[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"

$excludeDirs = @(
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "node_modules",
    "dist",
    "build"
)

function Test-IsExcludedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputPath
    )

    $segments = $InputPath -split "[\\/]"
    foreach ($segment in $segments) {
        if ($excludeDirs -contains $segment) {
            return $true
        }
    }

    return $false
}

$resolvedSource = (Resolve-Path -LiteralPath $Path).Path
$sourceItem = Get-Item -LiteralPath $resolvedSource
if (-not $sourceItem.PSIsContainer) {
    throw "Path must be a folder: $resolvedSource"
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folderName = Split-Path -Path $resolvedSource -Leaf
$downloadsDir = Join-Path -Path ([Environment]::GetFolderPath("UserProfile")) -ChildPath "Downloads"
if (-not (Test-Path -LiteralPath $downloadsDir)) {
    New-Item -ItemType Directory -Path $downloadsDir | Out-Null
}

$zipName = "{0}_{1}.zip" -f $folderName, $timestamp
$zipPath = Join-Path -Path $downloadsDir -ChildPath $zipName

$stagingRoot = Join-Path -Path $env:TEMP -ChildPath ("rag_zip_stage_{0}" -f ([guid]::NewGuid().ToString("N")))
New-Item -ItemType Directory -Path $stagingRoot | Out-Null

try {
    $files = Get-ChildItem -LiteralPath $resolvedSource -Recurse -File -Force |
        Where-Object { -not (Test-IsExcludedPath -InputPath $_.FullName) }

    $sourceWithSlash = $resolvedSource.TrimEnd("\") + "\"
    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($sourceWithSlash.Length)
        $targetPath = Join-Path -Path $stagingRoot -ChildPath $relativePath
        $targetDir = Split-Path -Path $targetPath -Parent
        if (-not (Test-Path -LiteralPath $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir | Out-Null
        }
        Copy-Item -LiteralPath $file.FullName -Destination $targetPath -Force
    }

    if (Test-Path -LiteralPath $zipPath) {
        Remove-Item -LiteralPath $zipPath -Force
    }

    Compress-Archive -Path (Join-Path $stagingRoot "*") -DestinationPath $zipPath -CompressionLevel Optimal
    Write-Output $zipPath
}
finally {
    if (Test-Path -LiteralPath $stagingRoot) {
        Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    }
}
