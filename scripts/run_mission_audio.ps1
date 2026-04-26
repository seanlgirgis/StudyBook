param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Script,
    [string]$Slug,
    [int]$ChunkSize = 750,
    [string]$TempRoot = "D:\temp\studybook_audio",
    [switch]$SkipEnvSetter,
    [int]$RequestTimeoutSeconds = 120
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ScriptPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputPath,
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    if ([System.IO.Path]::IsPathRooted($InputPath)) {
        return [System.IO.Path]::GetFullPath($InputPath)
    }
    return [System.IO.Path]::GetFullPath((Join-Path -Path $RepoRoot -ChildPath $InputPath))
}

function Resolve-SlugFromScriptPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptPath
    )

    $stem = [System.IO.Path]::GetFileNameWithoutExtension($ScriptPath)
    if ($stem -like "audio_script_*") {
        return $stem.Substring("audio_script_".Length)
    }
    return ($stem -replace "[^A-Za-z0-9._-]+", "-").Trim("-")
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$envSetter = Join-Path $repoRoot "env_setter.ps1"
$generator = Join-Path $repoRoot "temp\jobsearch\scripts\generate_audio_generic.py"

if (-not (Test-Path -LiteralPath $generator)) {
    throw "Missing generator script: $generator"
}

$scriptPath = Resolve-ScriptPath -InputPath $Script -RepoRoot $repoRoot
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Input script not found: $scriptPath"
}

$finalSlug = if ([string]::IsNullOrWhiteSpace($Slug)) {
    Resolve-SlugFromScriptPath -ScriptPath $scriptPath
} else {
    $Slug.Trim()
}

if ([string]::IsNullOrWhiteSpace($finalSlug)) {
    throw "Could not resolve slug from script name. Pass -Slug explicitly."
}

$runRoot = Join-Path $TempRoot $finalSlug
$clipsDir = Join-Path $runRoot "audio_clips"
New-Item -ItemType Directory -Force -Path $clipsDir | Out-Null

Push-Location $repoRoot
try {
    $preloadedKey = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "Process")
    $hasPreloadedKey = -not [string]::IsNullOrWhiteSpace($preloadedKey)

    if (-not $SkipEnvSetter -and -not $hasPreloadedKey) {
        if (-not (Test-Path -LiteralPath $envSetter)) {
            throw "Missing env_setter.ps1 at: $envSetter"
        }
        . $envSetter -NonInteractive
    }
    elseif ($hasPreloadedKey) {
        Write-Host "OPENAI_API_KEY already present in current shell; skipping env_setter.ps1." -ForegroundColor DarkGray
    }

    $keyLoaded = python -c "import os; print(bool(os.getenv('OPENAI_API_KEY')))"
    if ($keyLoaded -notmatch "True") {
        throw "OPENAI_API_KEY not loaded. env_setter.ps1 may have failed."
    }

    Write-Host "Generating clips..." -ForegroundColor Cyan
    python $generator `
        --script $scriptPath `
        --output $clipsDir `
        --chunk-size $ChunkSize `
        --request-timeout-seconds $RequestTimeoutSeconds

    if ($LASTEXITCODE -ne 0) {
        throw "Audio generation failed with exit code $LASTEXITCODE"
    }

    $mp3Files = @(Get-ChildItem -Path $clipsDir -Filter "*.mp3" | Sort-Object Name)
    if ($mp3Files.Count -eq 0) {
        throw "No MP3 clips were generated in $clipsDir"
    }

    $fileListPath = Join-Path $clipsDir "filelist.txt"
    $mp3Files | ForEach-Object { "file '$($_.FullName)'" } | Out-File -Encoding utf8 $fileListPath

    $finalPath = Join-Path $runRoot ("final_{0}.mp3" -f $finalSlug)
    if (Test-Path -LiteralPath $finalPath) {
        Remove-Item -LiteralPath $finalPath -Force
    }

    Write-Host "Stitching final MP3..." -ForegroundColor Cyan
    ffmpeg -f concat -safe 0 -i $fileListPath -c copy $finalPath
    if ($LASTEXITCODE -ne 0) {
        throw "ffmpeg stitching failed with exit code $LASTEXITCODE"
    }

    if (-not (Test-Path -LiteralPath $finalPath)) {
        throw "Final MP3 was not created: $finalPath"
    }

    $sizeBytes = (Get-Item -LiteralPath $finalPath).Length
    $duration = ffprobe -v quiet -show_entries format=duration -of csv=p=0 $finalPath

    $uploadInstructionsPath = Join-Path $runRoot "UPLOAD_INSTRUCTIONS.md"
    $url = "https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{0}.mp3" -f $finalSlug
    $uploadContent = @"
# R2 Upload Instructions - $finalSlug

## File to upload
$finalPath

## Target filename on R2
final_$finalSlug.mp3

## Expected public URL after upload
$url

## Steps
1. Open Cloudflare R2 dashboard.
2. Upload final_$finalSlug.mp3 to the learning hub media bucket.
3. Open the public URL and confirm playback.
4. Tell Codex the upload is complete and which HTML page should be updated.
"@
    Set-Content -Path $uploadInstructionsPath -Value $uploadContent

    Write-Host ""
    Write-Host "Done." -ForegroundColor Green
    Write-Host "Slug:         $finalSlug"
    Write-Host "Clips:        $($mp3Files.Count) files"
    Write-Host "Final file:   $finalPath"
    Write-Host "Size bytes:   $sizeBytes"
    Write-Host "Duration sec: $duration"
    Write-Host "Upload guide: $uploadInstructionsPath"
}
finally {
    Pop-Location
}
