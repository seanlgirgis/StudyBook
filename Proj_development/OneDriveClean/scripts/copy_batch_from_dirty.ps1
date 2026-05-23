param(
  [Parameter(Mandatory = $true)]
  [string]$BatchName,
  [switch]$NoPrompt
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
$remotes = Read-JsonConfig (Join-Path $repoRoot "config/rclone_remotes.local.json") (Join-Path $repoRoot "config/rclone_remotes.example.json")
$batches = Read-JsonConfig (Join-Path $repoRoot "config/batches.local.json") (Join-Path $repoRoot "config/batches.example.json")

$batchConfig = $batches.batches.$BatchName
if (-not $batchConfig) { throw "Batch '$BatchName' not found in batches config" }
$remotePath = [string]$batchConfig.remote_path
if ([string]::IsNullOrWhiteSpace($remotePath)) { throw "remote_path missing for '$BatchName'" }

$src = "{0}:{1}" -f [string]$remotes.dirty_remote, $remotePath
$dest = Join-Path (Join-Path $paths.lab_root $paths.hydrated_dir) $BatchName
$logDir = Join-Path $paths.lab_root $paths.logs_dir
New-Item -ItemType Directory -Force -Path $dest | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir ("{0}_copy.log" -f $BatchName)

Write-Host "Source: $src"
Write-Host "Destination: $dest"
Write-Host "Log: $logFile"
Write-Host "Mode: rclone copy (no sync)"

if (-not $NoPrompt) {
  $answer = Read-Host "Proceed with copy? (yes/no)"
  if ($answer -ne "yes") { throw "Copy aborted by user" }
}

rclone copy $src $dest --progress --log-file $logFile
Write-Host "Batch copy complete"
