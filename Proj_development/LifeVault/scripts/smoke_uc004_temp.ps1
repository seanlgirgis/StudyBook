param(
  [string]$TempRoot
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$srcPath = Join-Path $projectRoot "src"

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "$srcPath;$($env:PYTHONPATH)"
} else {
  $env:PYTHONPATH = $srcPath
}

function Resolve-SmokeRoot {
  param([string]$OverrideRoot)
  if ($OverrideRoot) {
    return $OverrideRoot
  }

  $dTemp = "D:\\temp"
  try {
    if (-not (Test-Path $dTemp)) {
      New-Item -ItemType Directory -Force -Path $dTemp | Out-Null
    }
    if (Test-Path $dTemp) {
      return (Join-Path $dTemp "lifevault_uc004_smoke")
    }
  } catch {
    # fall through to TEMP
  }

  return (Join-Path $env:TEMP "lifevault_uc004_smoke")
}

$base = Resolve-SmokeRoot -OverrideRoot $TempRoot
$dbDir = Join-Path $base "db"
$podDir = Join-Path $base "pod_fake"
$dbPath = Join-Path $dbDir "temp_uc004.sqlite"

New-Item -ItemType Directory -Force -Path $base,$dbDir,$podDir | Out-Null
Write-Host "UC_004 smoke temp root: $base"
New-Item -ItemType Directory -Force -Path (Join-Path $podDir "original_copies\nested"), (Join-Path $podDir "reports") | Out-Null

Set-Content -Path (Join-Path $podDir "original_copies\alpha.txt") -Value "fake alpha" -Encoding UTF8
Set-Content -Path (Join-Path $podDir "original_copies\nested\beta.txt") -Value "fake beta" -Encoding UTF8

$utcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$profile = @{
  schema_version = "1.0"
  pod_id = "pod_uc004_smoke"
  created_at = $utcNow
  source_path = (Join-Path $base "fake_source")
  source_proposal_id = "uc001_smoke"
  source_proposal_path = (Join-Path $podDir "_source_proposal_snapshot.json")
  story = "UC_004 temp smoke pod"
  project = "Smoke"
  category = "Test"
  event_name = "uc004_smoke"
  suggested_vault_path = "LifeVault/01_Knowledge"
  pod_status = "created"
  sensitivity_highest_level = "normal"
  file_count = 2
  copied_file_count = 2
  failed_copy_count = 0
  duplicate_candidate_count = 1
  content_scan_status = "not_performed"
  database_index_status = "not_indexed"
  vault_publish_status = "not_published"
  notes = "temp smoke"
  warnings = @()
  errors = @()
}
$profile | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $podDir "_pod_profile.json") -Encoding utf8NoBOM

@"
pod_id,source_relative_path,source_absolute_path,pod_relative_path,pod_absolute_path,filename,extension,size_bytes,modified_time,copied_at,filename_sensitivity_level,filename_sensitivity_reasons,duplicate_name_group_id,copy_status,copy_error
pod_uc004_smoke,alpha.txt,$base\fake_source\alpha.txt,original_copies/alpha.txt,$podDir\original_copies\alpha.txt,alpha.txt,.txt,10,$utcNow,$utcNow,normal,no_sensitive_rule_match,dup_name_001,copied,
pod_uc004_smoke,nested/beta.txt,$base\fake_source\nested\beta.txt,original_copies/nested/beta.txt,$podDir\original_copies\nested\beta.txt,beta.txt,.txt,9,$utcNow,$utcNow,normal,no_sensitive_rule_match,dup_name_001,copied,
"@ | Set-Content -Path (Join-Path $podDir "_pod_manifest.csv") -Encoding utf8NoBOM

@"
pod_id,pod_relative_path,filename,suggested_sensitivity_level,user_sensitivity_level,review_decision,user_notes,approved_for_database_index,approved_for_vault_publish
pod_uc004_smoke,original_copies/alpha.txt,alpha.txt,normal,,needs_review,,false,false
pod_uc004_smoke,original_copies/nested/beta.txt,beta.txt,normal,,needs_review,,false,false
"@ | Set-Content -Path (Join-Path $podDir "_review.csv") -Encoding utf8NoBOM

$snapshot = @{
  proposal_id = "uc001_smoke"
  source_path = "C:\\temp\\fake_source"
  scan_status = "success"
}
$snapshot | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $podDir "_source_proposal_snapshot.json") -Encoding utf8NoBOM

python -m lifevault.migrate --db-path "$dbPath" --apply 0001_lifevault_core_schema
if ($LASTEXITCODE -ne 0) { throw "Migration apply failed" }

$dryOut = python -m lifevault.uc004_cli --pod-path "$podDir" --db-path "$dbPath" --dry-run
if ($LASTEXITCODE -ne 0) { throw "UC_004 dry-run failed" }

$approvedOut = python -m lifevault.uc004_cli --pod-path "$podDir" --db-path "$dbPath" --approved
if ($LASTEXITCODE -ne 0) { throw "UC_004 approved indexing failed" }

$queryOut = @"
import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])
for table in ["sources","pods","files","file_instances","review_decisions","audit_log"]:
    c = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}={c}")
conn.close()
"@ | python - "$dbPath"
if ($LASTEXITCODE -ne 0) { throw "Count query failed" }

Write-Host "DB path: $dbPath"
Write-Host "`nUC_004 dry-run summary:"
$dryOut | ForEach-Object { Write-Host $_ }
Write-Host "`nUC_004 approved index summary:"
$approvedOut | ForEach-Object { Write-Host $_ }
Write-Host "`nIndexed row counts:"
$queryOut | ForEach-Object { Write-Host $_ }
