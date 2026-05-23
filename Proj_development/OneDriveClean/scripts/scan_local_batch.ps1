param(
  [Parameter(Mandatory = $true)]
  [string]$BatchName
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

function Read-JsonConfig($localPath, $examplePath) {
  if (Test-Path $localPath) { return Get-Content -Raw $localPath | ConvertFrom-Json }
  if (Test-Path $examplePath) { return Get-Content -Raw $examplePath | ConvertFrom-Json }
  throw "Missing config: $localPath or $examplePath"
}

$paths = Read-JsonConfig (Join-Path $repoRoot "config/paths.local.json") (Join-Path $repoRoot "config/paths.example.json")

$batchPath = Join-Path (Join-Path $paths.lab_root $paths.hydrated_dir) $BatchName
$reportPath = Join-Path (Join-Path $paths.lab_root $paths.reports_dir) $BatchName

if (-not (Test-Path $batchPath)) { throw "Batch folder not found: $batchPath" }
New-Item -ItemType Directory -Force -Path $reportPath | Out-Null

python -m onedriveclean.reports --batch-name $BatchName
Write-Host "Scan/report complete for: $BatchName"
Write-Host "Reports: $reportPath"
