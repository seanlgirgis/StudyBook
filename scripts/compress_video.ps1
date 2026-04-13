param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputFile,

    [string]$OutputFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-Ffmpeg {
    $cmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw "ffmpeg not found on PATH. Open a new shell after install and retry."
}

$inputPath = [System.IO.Path]::GetFullPath($InputFile)
if (-not (Test-Path -LiteralPath $inputPath)) {
    throw "Input file not found: $inputPath"
}

$dir = Split-Path -Path $inputPath -Parent
$base = [System.IO.Path]::GetFileNameWithoutExtension($inputPath)
$outPath = if ([string]::IsNullOrWhiteSpace($OutputFile)) {
    Join-Path -Path $dir -ChildPath "${base}_small.mp4"
} else {
    [System.IO.Path]::GetFullPath($OutputFile)
}

$ffmpeg = Resolve-Ffmpeg
Write-Host "Input : $inputPath" -ForegroundColor Gray
Write-Host "Output: $outPath" -ForegroundColor Gray
Write-Host "Profile: medium video compression (H.264 CRF 24, preset slow, AAC 96k)" -ForegroundColor Cyan

& $ffmpeg -y -i $inputPath -c:v libx264 -crf 24 -preset slow -c:a aac -b:a 96k $outPath
if ($LASTEXITCODE -ne 0) {
    throw "ffmpeg failed with exit code $LASTEXITCODE"
}

Write-Host "Done: $outPath" -ForegroundColor Green
