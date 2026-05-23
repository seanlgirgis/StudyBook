$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  param([string]$ScriptDir)
  Resolve-Path (Join-Path $ScriptDir "..\..")
}

function Read-JsonConfig {
  param([string]$LocalPath, [string]$ExamplePath)
  if (Test-Path $LocalPath) { return Get-Content -Raw $LocalPath | ConvertFrom-Json }
  if (Test-Path $ExamplePath) { return Get-Content -Raw $ExamplePath | ConvertFrom-Json }
  throw "Missing config: $LocalPath or $ExamplePath"
}

function Get-LabContext {
  param([string]$ScriptDir, [string]$LabName)
  $repoRoot = Get-RepoRoot -ScriptDir $ScriptDir
  $paths = Read-JsonConfig (Join-Path $repoRoot "config/paths.local.json") (Join-Path $repoRoot "config/paths.example.json")
  $remotes = Read-JsonConfig (Join-Path $repoRoot "config/rclone_remotes.local.json") (Join-Path $repoRoot "config/rclone_remotes.example.json")

  $labRunsRoot = Join-Path ([string]$paths.lab_root) ([string]$paths.lab_runs_dir)
  $runDir = Join-Path $labRunsRoot $LabName
  New-Item -ItemType Directory -Force -Path $runDir | Out-Null

  [PSCustomObject]@{
    RepoRoot = $repoRoot
    Paths = $paths
    Remotes = $remotes
    LabRunsRoot = $labRunsRoot
    RunDir = $runDir
  }
}

function Get-RcloneExcludeArgs {
  param($RemotesConfig)
  $args = @()
  if ($null -eq $RemotesConfig) { return $args }
  $excluded = $RemotesConfig.excluded_remote_paths
  if ($null -eq $excluded) { return $args }
  foreach ($pattern in @($excluded)) {
    if (-not [string]::IsNullOrWhiteSpace([string]$pattern)) {
      $args += "--exclude"
      $args += [string]$pattern
    }
  }
  return $args
}
