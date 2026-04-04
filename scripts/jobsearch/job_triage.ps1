param(
    [string]$InputTextPath = ".\intake\intake.md",
    [string]$Company = "",
    [string]$Role = "",
    [string]$Location = "",
    [double]$SimilarityThreshold = 0.80,
    [string]$OutputPath = "data/jobs/_triage/latest_triage.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$inputPath = if ([System.IO.Path]::IsPathRooted($InputTextPath)) { $InputTextPath } else { Join-Path $root $InputTextPath }
if (-not (Test-Path -LiteralPath $inputPath)) { throw "Input text file not found: $inputPath" }

$text = Get-Content -Raw -LiteralPath $inputPath -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($text)) { throw "Input text is empty: $inputPath" }

if ([string]::IsNullOrWhiteSpace($Company)) {
    if ($text -match "(?im)^([A-Za-z0-9&'\-\., ]{2,})\s*$") { $Company = $Matches[1].Trim() }
}
if ([string]::IsNullOrWhiteSpace($Role)) {
    if ($text -match "(?im)^([A-Za-z0-9&'\-\.,/\(\) ]*Data Engineer[A-Za-z0-9&'\-\.,/\(\) ]*)\s*$") { $Role = $Matches[1].Trim() }
}
if ([string]::IsNullOrWhiteSpace($Location)) {
    if ($text -match "(?im)(Dallas[^\n\r]*|McKinney[^\n\r]*|Dallas-Fort Worth[^\n\r]*)") { $Location = $Matches[1].Trim() }
}

$stop = @('the','and','for','with','this','that','from','into','your','you','are','our','will','have','has','was','were','about','role','job','data','engineer','years','experience','work','team','position','skills','strong','plus','nice','must','able','using','across','through','support','build')
$stopSet = @{}
foreach($w in $stop){ $stopSet[$w] = $true }

function Get-TermSet([string]$s) {
    $set = @{}
    $tokens = [regex]::Matches($s.ToLowerInvariant(), "[a-z0-9\+#\-]{3,}")
    foreach($m in $tokens){
        $t = $m.Value
        if (-not $stopSet.ContainsKey($t)) { $set[$t] = $true }
    }
    return $set
}

function Get-Jaccard($a, $b) {
    if ($a.Count -eq 0 -or $b.Count -eq 0) { return 0.0 }
    $inter = 0
    foreach($k in $a.Keys){ if ($b.ContainsKey($k)) { $inter++ } }
    $union = $a.Count + $b.Count - $inter
    if ($union -le 0) { return 0.0 }
    return [math]::Round(($inter / $union), 4)
}

$queryTerms = Get-TermSet $text
$jobsRoot = Join-Path $root "data/jobs"
$metaFiles = Get-ChildItem -Path $jobsRoot -Recurse -Filter "metadata.yaml" -File -ErrorAction SilentlyContinue

$exactAppliedHit = $null
$similarityRows = @()

foreach($mf in $metaFiles){
    $jobDir = Split-Path $mf.FullName -Parent
    $meta = Get-Content -Raw -LiteralPath $mf.FullName -Encoding UTF8

    $mCompany = ""
    $mRole = ""
    $mApplied = $false
    $mJobId = Split-Path $jobDir -Leaf

    if ($meta -match "(?im)^company:\s*(.+)$") { $mCompany = $Matches[1].Trim().Trim("'") }
    if ($meta -match "(?im)^role:\s*(.+)$") { $mRole = $Matches[1].Trim().Trim("'") }
    if ($meta -match "(?im)^\s*applied:\s*true\s*$") { $mApplied = $true }

    if ($mApplied -and -not [string]::IsNullOrWhiteSpace($Company) -and -not [string]::IsNullOrWhiteSpace($Role)) {
        $cMatch = ($mCompany.ToLowerInvariant() -eq $Company.ToLowerInvariant())
        $rMatch = ($mRole.ToLowerInvariant() -eq $Role.ToLowerInvariant())
        if ($cMatch -and $rMatch) {
            $exactAppliedHit = [pscustomobject]@{ job_id=$mJobId; company=$mCompany; role=$mRole }
        }
    }

    $rawPath = Join-Path $jobDir "raw\raw_intake.md"
    if ($mApplied -and (Test-Path -LiteralPath $rawPath)) {
        $rawText = Get-Content -Raw -LiteralPath $rawPath -Encoding UTF8
        $sim = Get-Jaccard $queryTerms (Get-TermSet $rawText)
        if ($sim -gt 0) {
            $similarityRows += [pscustomobject]@{ job_id=$mJobId; company=$mCompany; role=$mRole; similarity=$sim }
        }
    }
}

$topSimilar = $similarityRows | Sort-Object similarity -Descending | Select-Object -First 5
$maxSimilarity = if ($topSimilar) { [double]$topSimilar[0].similarity } else { 0.0 }

$fit = 50
$reasons = New-Object System.Collections.Generic.List[string]

$signals = @(
    @{k='aws'; p=8; msg='AWS stack match'},
    @{k='python'; p=7; msg='Python match'},
    @{k='sql'; p=7; msg='SQL match'},
    @{k='pipeline'; p=7; msg='Pipeline/ETL match'},
    @{k='etl'; p=5; msg='ETL keyword match'},
    @{k='glue'; p=6; msg='Glue match'},
    @{k='athena'; p=5; msg='Athena match'},
    @{k='s3'; p=4; msg='S3 match'},
    @{k='data lake'; p=4; msg='Data lake match'},
    @{k='data warehouse'; p=4; msg='Data warehouse match'},
    @{k='dallas'; p=3; msg='Location match Dallas'},
    @{k='mckinney'; p=3; msg='Location match McKinney'},
    @{k='hybrid'; p=2; msg='Hybrid match'}
)

$lower = $text.ToLowerInvariant()
foreach($s in $signals){
    if ($lower.Contains($s.k)) { $fit += $s.p; $reasons.Add($s.msg) }
}

if ($lower.Contains('junior')) {
    $fit -= 8
    $reasons.Add('Potential level mismatch (junior role)')
}

if ($fit -gt 95) { $fit = 95 }
if ($fit -lt 0) { $fit = 0 }

$decision = 'APPLY'
$decisionReason = 'Good fit and no duplicate blockers.'
if ($exactAppliedHit) {
    $decision = 'SKIP'
    $decisionReason = "Exact applied match already exists ($($exactAppliedHit.job_id))."
} elseif ($maxSimilarity -ge $SimilarityThreshold) {
    $decision = 'HOLD'
    $decisionReason = "High similarity to previously applied job (max=$maxSimilarity). Manual review recommended."
} elseif ($fit -lt 62) {
    $decision = 'HOLD'
    $decisionReason = "Fit score ($fit) below apply threshold."
}

$result = [ordered]@{
    triage_timestamp = (Get-Date).ToString('s')
    input_path = $inputPath
    company = $Company
    role = $Role
    location = $Location
    fit_score = $fit
    decision = $decision
    decision_reason = $decisionReason
    exact_applied_match = $exactAppliedHit
    max_similarity_applied = $maxSimilarity
    top_similar_applied = @($topSimilar)
    supporting_reasons = @($reasons)
}

$outAbs = if ([System.IO.Path]::IsPathRooted($OutputPath)) { $OutputPath } else { Join-Path $root $OutputPath }
$outDir = Split-Path -Path $outAbs -Parent
if ($outDir) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
($result | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $outAbs -Encoding UTF8

Write-Host "Triage complete:" -ForegroundColor Green
Write-Host "  Decision: $decision" -ForegroundColor Cyan
Write-Host "  Fit score: $fit" -ForegroundColor Gray
Write-Host "  Max similarity(applied): $maxSimilarity" -ForegroundColor Gray
Write-Host "  Output: $outAbs" -ForegroundColor Gray
