param(
  [string]$ProjectRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

function Resolve-ConfigPath {
  param([string]$Root)
  $local = Join-Path $Root "config\paths.local.json"
  $example = Join-Path $Root "config\paths.example.json"
  if (Test-Path $local) { return $local }
  if (Test-Path $example) { return $example }
  throw "No paths config found. Expected config\\paths.local.json or config\\paths.example.json"
}

$configPath = Resolve-ConfigPath -Root $ProjectRoot
$config = Get-Content -Raw $configPath | ConvertFrom-Json

$root = $config.lab_root
if (-not $root) { throw "paths config missing lab_root" }

$dirs = @(
  $config.onboarding_dir,
  $config.pods_dir,
  $config.proposals_dir,
  $config.db_dir,
  $config.reports_dir,
  $config.logs_dir,
  $config.exports_dir,
  $config.text_cache_dir
) | Where-Object { $_ -and $_.Trim().Length -gt 0 } | Select-Object -Unique

New-Item -ItemType Directory -Force -Path $root | Out-Null
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path (Join-Path $root $d) | Out-Null
}

Write-Host "LifeVault operational folders ensured under $root"