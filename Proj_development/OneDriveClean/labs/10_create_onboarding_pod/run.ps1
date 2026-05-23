$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..\..")

$tempSource = Join-Path $env:TEMP "odc_lab10_source"
if (Test-Path $tempSource) { Remove-Item -Recurse -Force $tempSource }
New-Item -ItemType Directory -Force -Path $tempSource | Out-Null
Set-Content -Encoding UTF8 (Join-Path $tempSource "doc1.md") "hello"
Set-Content -Encoding UTF8 (Join-Path $tempSource "doc2.pdf") "pdf"

$podId = & (Join-Path $repoRoot "scripts\create_onboarding_pod.ps1") -SourcePath $tempSource -PodName "lab10_demo" -Project "Lab" -Category "demo" -EventName "lab10" -SuggestedVaultPath "FileStore/99_Labs/Lab10"
if (-not $podId) { throw "pod create failed" }

$pathsCfg = if (Test-Path (Join-Path $repoRoot "config\paths.local.json")) { Join-Path $repoRoot "config\paths.local.json" } else { Join-Path $repoRoot "config\paths.example.json" }
$cfg = Get-Content -Raw $pathsCfg | ConvertFrom-Json
$podDir = Join-Path (Join-Path $cfg.lab_root $cfg.pods_dir) ($podId | Select-Object -Last 1)

$required = @("original_copies","reports","_pod_profile.json","_pod_manifest.csv","_review.csv","_notes.md")
foreach ($r in $required) {
  if (-not (Test-Path (Join-Path $podDir $r))) { throw "missing $r" }
}
Write-Host "lab10 ok: $podDir"
