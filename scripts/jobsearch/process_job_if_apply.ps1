param(
    [Parameter(Mandatory=$true)][string]$TriagePath,
    [string]$InputTextPath = ".\intake\intake.md",
    [string]$Company,
    [string]$Role,
    [string]$Location,
    [int]$JobNumber,
    [switch]$OverrideDecision
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$triageAbs = if ([System.IO.Path]::IsPathRooted($TriagePath)) { $TriagePath } else { Join-Path $root $TriagePath }
$inputAbs = if ([System.IO.Path]::IsPathRooted($InputTextPath)) { $InputTextPath } else { Join-Path $root $InputTextPath }

if (-not (Test-Path -LiteralPath $triageAbs)) { throw "Triage file not found: $triageAbs" }
if (-not (Test-Path -LiteralPath $inputAbs)) { throw "Input text file not found: $inputAbs" }

$triage = Get-Content -Raw -LiteralPath $triageAbs -Encoding UTF8 | ConvertFrom-Json
if (-not $OverrideDecision -and $triage.decision -ne 'APPLY') {
    throw "Triage decision is '$($triage.decision)'. Use -OverrideDecision to proceed anyway."
}

$companyVal = if ($Company) { $Company } elseif ($triage.company) { [string]$triage.company } else { 'Unknown' }
$roleVal = if ($Role) { $Role } elseif ($triage.role) { [string]$triage.role } else { 'Unknown' }
$locationVal = if ($Location) { $Location } elseif ($triage.location) { [string]$triage.location } else { 'Unknown' }

$jobsRoot = Join-Path $root 'data/jobs'
New-Item -ItemType Directory -Path $jobsRoot -Force | Out-Null

if ($JobNumber -le 0) {
    $max = 0
    Get-ChildItem -Path $jobsRoot -Directory | ForEach-Object {
        if ($_.Name -match '^(\d{5})_') {
            $n = [int]$Matches[1]
            if ($n -gt $max) { $max = $n }
        }
    }
    $JobNumber = $max + 1
}

$jobPrefix = ('{0:D5}' -f $JobNumber)
$uuid = [guid]::NewGuid().ToString()
$uuid8 = $uuid.Substring(0,8)
$jobId = "$jobPrefix`_$uuid8"
$jobDir = Join-Path $jobsRoot $jobId

@('raw','generated','score','tailored','research') | ForEach-Object {
    New-Item -ItemType Directory -Path (Join-Path $jobDir $_) -Force | Out-Null
}

Copy-Item -LiteralPath $inputAbs -Destination (Join-Path $jobDir 'intake.md') -Force
Copy-Item -LiteralPath $inputAbs -Destination (Join-Path $jobDir 'raw/raw_intake.md') -Force

$meta = @"
uuid: $uuid
job_id: $jobId
original_filename: intake.md
company: $companyVal
role: $roleVal
company_website: ''
location: $locationVal
status: READY
score: $($triage.fit_score)
recommendation: $($triage.decision)
score_date: '$((Get-Date).ToString('s'))'
created_at: '$((Get-Date).ToString('s'))'
notes: '$($triage.decision_reason)'
application:
  applied: false
  applied_date: null
  applied_method: null
  application_notes: ''
  history:
  - date: '$((Get-Date).ToString('yyyy-MM-dd'))'
    status: Created
    notes: Created from triage gate ($($triage.decision))
"@
Set-Content -LiteralPath (Join-Path $jobDir 'metadata.yaml') -Value $meta -Encoding UTF8

Write-Host "Job scaffold created:" -ForegroundColor Green
Write-Host "  job_id: $jobId"
Write-Host "  uuid: $uuid"
Write-Host "  folder: $jobDir"
Write-Host "Next: generate intermediates then run renderers for resume.md/cover.md/resume.docx/cover.docx"
