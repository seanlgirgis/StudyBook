param(
  [Parameter(Mandatory=$true, Position=0)]
  [string]$SourcePath
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$env:PYTHONPATH = (Join-Path $repoRoot "src")

$code = @"
import json
from pathlib import Path
from onedriveclean.config import load_config
from onedriveclean.intake import analyze_source_folder, save_proposal

source = Path(r'$SourcePath')
cfg = load_config(Path(r'$repoRoot'))
proposal = analyze_source_folder(source)
proposals_dir = cfg.lab_path('onboarding_dir') / 'proposals'
out = save_proposal(proposals_dir, proposal)
print(json.dumps({'proposal_path': str(out), 'proposal': proposal.__dict__}, indent=2))
"@

$resultJson = python -c $code
if ($LASTEXITCODE -ne 0) { throw "Proposal generation failed" }

$result = $resultJson | ConvertFrom-Json
$proposalPath = [string]$result.proposal_path
$p = $result.proposal

Write-Host "Proposal saved:" $proposalPath
Write-Host "--- Pod Proposal ---"
Write-Host "source_path:" $p.source_path
Write-Host "file_count:" $p.file_count
Write-Host "total_size_bytes:" $p.total_size_bytes
Write-Host "suggested_pod_name:" $p.suggested_pod_name
Write-Host "suggested_project:" $p.suggested_project
Write-Host "suggested_category:" $p.suggested_category
Write-Host "suggested_event_name:" $p.suggested_event_name
Write-Host "suggested_vault_path:" $p.suggested_vault_path
Write-Host "confidence:" $p.confidence
Write-Host "reason:" $p.reason
Write-Host "questions_for_user:" ($p.questions_for_user -join " | ")

$choice = Read-Host "Choose: [A]ccept, [E]dit, [S]ave-only, [Q]uit"
$choice = $choice.ToUpperInvariant()

if ($choice -eq "Q") {
  Write-Host "Quit without pod creation. Proposal saved at $proposalPath"
  exit 0
}
if ($choice -eq "S") {
  Write-Host "Saved proposal only: $proposalPath"
  exit 0
}

$podName = [string]$p.suggested_pod_name
$project = [string]$p.suggested_project
$category = [string]$p.suggested_category
$eventName = [string]$p.suggested_event_name
$vpath = [string]$p.suggested_vault_path

if ($choice -eq "E") {
  $v = Read-Host "PodName [$podName]"; if ($v) { $podName = $v }
  $v = Read-Host "Project [$project]"; if ($v) { $project = $v }
  $v = Read-Host "Category [$category]"; if ($v) { $category = $v }
  $v = Read-Host "EventName [$eventName]"; if ($v) { $eventName = $v }
  $v = Read-Host "SuggestedVaultPath [$vpath]"; if ($v) { $vpath = $v }
}

$podId = & (Join-Path $repoRoot "scripts\create_onboarding_pod.ps1") -SourcePath $SourcePath -PodName $podName -Project $project -Category $category -EventName $eventName -SuggestedVaultPath $vpath
if ($LASTEXITCODE -ne 0) { throw "Pod creation failed" }
Write-Host "Pod created:" $podId
