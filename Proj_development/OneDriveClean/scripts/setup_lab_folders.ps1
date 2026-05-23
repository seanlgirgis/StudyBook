$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

$pathsLocal = Join-Path $repoRoot "config/paths.local.json"
$pathsExample = Join-Path $repoRoot "config/paths.example.json"
$configPath = if (Test-Path $pathsLocal) { $pathsLocal } elseif (Test-Path $pathsExample) { $pathsExample } else { throw "Missing paths config" }
$cfg = Get-Content -Raw $configPath | ConvertFrom-Json

$labRoot = [string]$cfg.lab_root
$dirs = @(
  [string]$cfg.inventory_dir,
  [string]$cfg.hydrated_dir,
  [string]$cfg.staging_dir,
  [string]$cfg.db_dir,
  [string]$cfg.onboarding_dir,
  [string]$cfg.pods_dir,
  [string]$cfg.reports_dir,
  [string]$cfg.logs_dir
)

New-Item -ItemType Directory -Force -Path $labRoot | Out-Null
foreach ($d in $dirs) {
  $target = Join-Path $labRoot $d
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  Write-Host "Ready: $target"
}
Write-Host "Lab root: $labRoot"
Write-Host "Config: $configPath"
