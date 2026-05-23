$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

function Read-JsonConfig($localPath, $examplePath) {
  if (Test-Path $localPath) { return Get-Content -Raw $localPath | ConvertFrom-Json }
  if (Test-Path $examplePath) { return Get-Content -Raw $examplePath | ConvertFrom-Json }
  throw "Missing config: $localPath or $examplePath"
}
function Get-RcloneExcludeArgs($remotesConfig) {
  $args = @()
  $excluded = $remotesConfig.excluded_remote_paths
  if ($null -eq $excluded) { return $args }
  foreach ($pattern in @($excluded)) {
    if (-not [string]::IsNullOrWhiteSpace([string]$pattern)) {
      $args += "--exclude"
      $args += [string]$pattern
    }
  }
  return $args
}

$paths = Read-JsonConfig (Join-Path $repoRoot "config/paths.local.json") (Join-Path $repoRoot "config/paths.example.json")
$remotes = Read-JsonConfig (Join-Path $repoRoot "config/rclone_remotes.local.json") (Join-Path $repoRoot "config/rclone_remotes.example.json")

$inventoryDir = Join-Path $paths.lab_root $paths.inventory_dir
New-Item -ItemType Directory -Force -Path $inventoryDir | Out-Null

$remote = [string]$remotes.clean_remote
$excludeArgs = Get-RcloneExcludeArgs $remotes

rclone lsd "${remote}:" @excludeArgs | Out-File -Encoding UTF8 (Join-Path $inventoryDir "onedrive_clean_top_folders.txt")
rclone size "${remote}:" @excludeArgs | Out-File -Encoding UTF8 (Join-Path $inventoryDir "onedrive_clean_total_size.txt")

Write-Host "Clean inventory complete in: $inventoryDir"
